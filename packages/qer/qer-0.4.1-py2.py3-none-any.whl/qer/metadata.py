from __future__ import print_function

import functools
import io
import logging
import os
import sys
import tarfile
import tempfile
import types
import zipfile
import abc

import pkg_resources
import six
from six.moves import StringIO

from qer import utils
from qer.dists import DistInfo


class Extractor(six.with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def names(self):
        pass

    @abc.abstractmethod
    def open(self, filename, mode='r', encoding=None):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    def relative_opener(self, fake_root, directory):
        def inner_opener(filename, *args, **kwargs):
            archive_path = filename
            if os.path.abspath(filename):
                if filename.startswith(fake_root):
                    archive_path = os.path.relpath(filename, fake_root)
            return self.open(directory + '/' + archive_path, *args, **kwargs)
        return inner_opener

    def contents(self, name):
        return self.open(name, encoding='utf-8').read()


def parse_source_filename(full_filename):
    filename = full_filename
    filename = filename.replace('.tar.gz', '')
    filename = filename.replace('.zip', '')
    filename = filename.replace('.tgz', '')

    dash_parts = filename.split('-')
    version_start = None
    for idx, part in enumerate(dash_parts):
        if part[0].isdigit():
            version_start = idx
            break

    if version_start is None:
        return os.path.basename(full_filename), None

    if version_start == 0:
        raise ValueError('Package name missing: {}'.format(full_filename))

    pkg_name = '-'.join(dash_parts[:version_start])
    version = utils.parse_version('-'.join(dash_parts[version_start:]))

    return pkg_name, version


class NonExtractor(Extractor):
    def __init__(self, path):
        self.path = path
        self.io_open = io.open

    def names(self):
        parent_dir = os.path.abspath(os.path.join(self.path, '..'))
        for root, dirs, files in os.walk(self.path):
            rel_root = os.path.relpath(root, parent_dir).replace('\\', '/')
            for file in files:
                yield rel_root + '/' + file

    def open(self, filename, mode='r', encoding='utf-8'):
        parent_dir = os.path.abspath(os.path.join(self.path, '..'))
        return self.io_open(os.path.join(parent_dir, filename), mode=mode, encoding=encoding)

    def close(self):
        pass


class TarExtractor(Extractor):
    def __init__(self, filename):
        self.tar = tarfile.open(filename, 'r:gz')
        self.io_open = io.open

    def names(self):
        return (info.name for info in self.tar.getmembers())

    def open(self, filename, mode='r', encoding='utf-8'):
        filename = filename.replace('\\', '/').replace('./', '')
        if not os.path.isabs(filename):
            try:
                handle = self.tar.extractfile(filename)
                return with_decoding(handle, encoding=encoding if mode != 'rb' else None)
            except KeyError:
                raise IOError('Not found in archive: {}'.format(filename))
        else:
            return self.io_open(filename, mode=mode, encoding=encoding)

    def close(self):
        self.tar.close()


class ZipExtractor(Extractor):
    def __init__(self, filename):
        self.zfile = zipfile.ZipFile(filename, 'r')
        self.io_open = io.open

    def names(self):
        return self.zfile.namelist()

    def open(self, filename, mode='r', encoding='utf-8'):
        filename = filename.replace('\\', '/').replace('./', '')
        if not os.path.isabs(filename):
            try:
                output = with_decoding(StringIO(self.zfile.read(filename).decode(encoding)), None)
                return output
            except KeyError:
                raise IOError('Not found in archive: {}'.format(filename))
        else:
            return self.io_open(filename, mode=mode, encoding=encoding)

    def close(self):
        self.zfile.close()


def extract_metadata(dist, extras=()):
    """"""
    if dist.lower().endswith('.whl'):
        return _fetch_from_wheel(dist, extras=extras)
    if dist.lower().endswith('.zip'):
        return _fetch_from_source(dist, ZipExtractor, extras=extras)
    elif dist.lower().endswith('.tar.gz'):
        return _fetch_from_source(dist, TarExtractor, extras=extras)
    else:
        return _fetch_from_source(dist, NonExtractor, extras=extras)


def _fetch_from_source(source_file, extractor_type, extras):
    """

    Args:
        source_file (str): Source file
        extractor_type (type[Extractor]): Type of extractor to use
        extras:

    Returns:

    """
    extractor = extractor_type(source_file)  # type: Extractor
    filename = os.path.basename(source_file)
    name, version = parse_source_filename(filename)
    try:
        metadata_file = None
        pkg_info_file = None
        egg_info = None
        setup_file = None

        for info_name in extractor.names():
            if info_name.lower().endswith('pkg-info') and info_name.count('/') <= 1:
                pkg_info_file = info_name
            elif info_name.endswith('.egg-info/requires.txt'):
                egg_info = info_name
            elif info_name.endswith('metadata') and info_name.count('/') <= 1:
                metadata_file = info_name

            if info_name.endswith('setup.py') and info_name.count('/') <= 1:
                setup_file = info_name
                break

        results = None
        if egg_info:
            requires_contents = ''
            try:
                requires_contents = extractor.open(egg_info, encoding='utf-8').read()
            except KeyError:
                pass
            return _parse_requires_file(requires_contents,
                                        name,
                                        version,
                                        extras)

        if pkg_info_file:
            results = _parse_flat_metadata(extractor.open(pkg_info_file, encoding='utf-8').read(), extras)

        if (results is None or not results.reqs) and setup_file:
            fake_setupdir = tempfile.mkdtemp()
            setup_results = _parse_setup_py(name, fake_setupdir,
                                            extractor.relative_opener(fake_setupdir,
                                                                      os.path.dirname(setup_file)), extras)
            if setup_results is not None:
                if version is not None:
                    setup_results.version = version
                if results:
                    setup_results.version = results.version
                return setup_results
            elif results is not None:
                return results
            else:
                return None

        if metadata_file:
            return _parse_flat_metadata(extractor.open(metadata_file, encoding='utf-8').read(), extras)
    finally:
        extractor.close()


def _fetch_from_wheel(wheel, extras):
    zfile = zipfile.ZipFile(wheel, 'r')
    try:
        metadata_file = None
        infos = zfile.namelist()
        for info in infos:
            if info.lower().endswith('metadata'):
                metadata_file = info

        if metadata_file:
            return _parse_flat_metadata(zfile.read(metadata_file).decode('utf-8'), extras)
    finally:
        zfile.close()


def _parse_flat_metadata(contents, extras):
    name = None
    version = None
    raw_reqs = []

    for line in contents.split('\n'):
        if line.lower().startswith('name:'):
            name = line.split(':')[1].strip()
        if line.lower().startswith('version:'):
            version = utils.parse_version(line.split(':')[1].strip())
        if line.lower().startswith('requires-dist:'):
            raw_reqs.append(line.split(':')[1].strip())

    return DistInfo(name, version, list(utils.parse_requirements(raw_reqs)), extras=extras)


class with_decoding(object):
    def __init__(self, wrap, encoding):
        self.file = wrap
        self.encoding = encoding

    def read(self):
        results = self.file.read()
        if self.encoding:
            results = results.decode(self.encoding)
        elif six.PY2:
            results = str(''.join([i if ord(i) < 128 else ' ' for i in results]))
        return results

    def readlines(self):
        results = self.file.readlines()
        if self.encoding:
            results = [result.decode(self.encoding) for result in results]
        return results

    def write(self, *args, **kwargs):
        pass

    def __iter__(self):
        if self.encoding:
            return (line.decode(self.encoding) for line in self.file)
        return iter(self.file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass


def setup(results, *args, **kwargs):
    name = kwargs.get('name', None)
    version = kwargs.get('version', None)
    reqs = kwargs.get('install_requires', [])

    if isinstance(version, FakeModule):
        version = None

    if version is not None and version != '':
        version = pkg_resources.parse_version(str(version))

    results.append(DistInfo(name, version,
                            list(utils.parse_requirements(reqs))))
    return FakeModule('dist')


class FakeModule(types.ModuleType):
    call_count = 0

    def __getitem__(self, item):
        self.call_count += 1
        if self.call_count > 30:
            raise ValueError('Too many')
        return None

    def __contains__(self, item):
        return True

    def __getattr__(self, item):
        if isinstance(item, str):
            if item == '__path__':
                return ''
            elif item == '__file__':
                return os.path.join(self.__getattribute__('__name__'), '__init__.py')
            return FakeModule(item)
        else:
            return None


def fake_import(name, orig_import, modname, *args, **kwargs):
    try:
        if name.lower() == modname.lower():
            sys.modules[modname] = FakeModule(modname)
        return orig_import(modname, *args, **kwargs)
    except ImportError:
        # Skip any cython importing to improve setup.py compatibility (e.g. subprocess32)
        if 'Cython' in modname:
            raise

        modparts = modname.split('.')
        for idx, mod in enumerate(modparts):
            sys.modules['.'.join(modparts[:idx + 1])] = FakeModule(mod)
        return orig_import(modname, *args, **kwargs)


def _parse_setup_py(name, fake_setupdir, opener, extras):
    import setuptools
    import distutils.core
    import sys

    # Capture warnings.warn, which is sometimes used in setup.py files
    logging.captureWarnings(True)

    sys.exit = lambda code: None

    results = []
    setup_with_results = functools.partial(setup, results)
    if six.PY2:
        import __builtin__
        old_import = __builtin__.__import__
        __builtin__.__import__ = functools.partial(fake_import, name, __import__)
    else:
        import builtins
        old_import = builtins.__import__
        builtins.__import__ = functools.partial(fake_import, name, __import__)

    import imp
    old_load_source = imp.load_source
    imp.load_source = lambda *args, **kwargs: FakeModule('load_source')

    import codecs
    old_codecs_open = codecs.open
    codecs.open = opener

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stderr = StringIO()
    sys.stdout = StringIO()

    curr_dir = os.getcwd()

    old_open = io.open
    io.open = opener

    spy_globals = {'__file__': os.path.join(fake_setupdir, 'setup.py'),
                   '__name__': '__main__',
                   'open': opener,
                   'setup': setup_with_results}

    setuptools.setup = setup_with_results
    distutils.core.setup = setup_with_results
    contents = opener('setup.py', encoding='utf-8').read()
    try:
        if six.PY2:
            lines = contents.split('\n')
            lines = [line for line in lines if not (line.startswith('#') and
                                                    ('-*- coding' in line or '-*- encoding' in line))]
            contents = '\n'.join(lines)
        contents = contents.replace('print ', '')
        exec(contents, spy_globals, spy_globals)
    except:
        raise
    finally:
        os.chdir(curr_dir)
        io.open = old_open
        if six.PY2:
            __builtin__.__import__ = old_import
        else:
            builtins.__import__ = old_import
        imp.load_source = old_load_source
        codecs.open = old_codecs_open

        sys.stderr = old_stderr
        sys.stdout = old_stdout
    if not results:
        pass
    return results[0]


def _parse_requires_file(contents, name, version, extras):
    reqs = []
    sections = list(pkg_resources.split_sections(contents))
    for section in sections:
        if section[0] is None:
            reqs.extend(utils.parse_requirements(section[1]))
        elif section[0].startswith(':python_version'):
            for req in section[1]:
                reqs.append(utils.parse_requirement(req + ' ' + section[0].replace(':', ';')))

    return DistInfo(name, version, reqs)
