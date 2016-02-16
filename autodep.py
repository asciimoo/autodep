import __builtin__
import logging
import pip
import site
from sys import exc_info

original_import = __builtin__.__import__

# TODO complete the list..
_ambiguous_modules = (
    '_winreg',  # WINDOWS
    'builtins',  # PY3
    'gnureadline',  # PY3
    'http',  # PY3
    'importlib',  # PY3 - ipython
    'org.python',  # JYTHON
    'queue',  # PY3
    'urllib',  # PY3 - pip
    'win32security',  # WIN - ipython
)

# TODO
_package_name_map = {'ndg': 'ndg-httpsclient'}


def yesno(question):
    return raw_input('[?] {0} [yn] '.format(question)).strip() == 'y'


def pip_install(package_name, interactive=True):
    package_name = package_name.split('.')[0]
    if package_name in _package_name_map:
        package_name = _package_name_map[package_name]
    pip_args = ['-q', 'install']
    pip_args.append(package_name)

    if interactive and not yesno('Missing package: "{0}". Do you want to install?'.format(package_name)):
        return -1

    pip_ret = pip.main(pip_args)

    if pip_ret != 0:
        if yesno('Pip cannot install package, maybe package name differs from module name. Try with another name?'):
            return pip_install(raw_input('package name: ').strip(), False)
    else:
        reload(site)

    return pip_ret


class Importer(object):
    def __init__(self):
        super(Importer, self).__init__()
        self.import_cache = {}

    def _import_cache(fn):
        def wrapper(self, module_name=None, globals=None, locals=None, fromlist=None, level=-1):
            key = (module_name, tuple(fromlist) if fromlist else fromlist, level)

            if key in self.import_cache:
                return self.import_cache[key]

            module = fn(self, module_name, globals, locals, fromlist, level)
            self.import_cache[key] = module
            return module
        return wrapper

    @_import_cache
    def _import(self, module_name=None, globals=None, locals=None, fromlist=None, level=-1):
        logging.debug('import %s - %s %d', module_name, fromlist, level)
        module = None
        try:
            module = original_import(module_name, globals, locals, fromlist, level)
        except ImportError:
            # cannot handle relative import
            if level > 0:
                raise

            for bm in _ambiguous_modules:
                if module_name.startswith(bm):
                    raise

            # see http://lucumr.pocoo.org/2011/9/21/python-import-blackbox/
            exc_type, exc_value, tb_root = exc_info()
            tb = tb_root
            while tb is not None:
                if tb.tb_frame.f_globals.get('__name__') == module_name:
                    raise exc_type, exc_value, tb_root
                tb = tb.tb_next

            if pip_install(module_name) != 0:
                raise
            module = self._import(module_name, globals, locals, fromlist, level)

        return module


custom_importer = Importer()

__builtin__.__import__ = custom_importer._import


def __main__():
    from sys import argv

    if len(argv) < 2:
        exit(1)

    if argv[1].endswith('.py'):
        m = original_import(argv[1][:-3], locals())
        if hasattr(m, '__main__'):
            m.__main__()


if __name__ == '__main__':
    __main__()
