'''
sinfo finds and prints version information for loaded modules in the current
session, Python, and the OS.
'''

import sys
import types
import platform
import inspect
from datetime import datetime

from stdlib_list import stdlib_list


def imports(environ):
    '''Find modules in an environment.'''
    for name, val in environ:
        # If the module was directly imported
        if isinstance(val, types.ModuleType):
            yield val.__name__
        # If something was imported from the module
        else:
            try:
                yield val.__module__.split('.')[0]
            except AttributeError:
                pass


def sinfo(print_na=True, print_os=True, print_std_lib=False,
          print_private_modules=False, print_sys_modules=False,
          print_jupyter=True, excludes=['builtins', 'sinfo']):
    '''
    Print version information for loaded modules in the current session,
    Python, and the OS.

    Parameters
    ----------
    print_na : bool
        Print module name even when no version number is found.
    print_os : bool
        Print OS information.
    print_std_lib : bool
        Print information for modules imported from the standard library.
    print_private_modules : bool
        Print information for private modules.
    print_sys_modules : bool
        Print information about system modules. This is often rather verbose.
    print_jupyter : bool
        Print information about the jupyter environment if called from a
        notebook.
    excludes : list
        Do not print version information for these modules.
    '''
    # Exclude std lib packages
    if not print_std_lib:
        try:
            std_modules = stdlib_list(version=platform.python_version()[:-2])
        except ValueError:
            # Use the latest available if the Python version cannot be found
            std_modules = stdlib_list('3.7')
        excludes = excludes + std_modules
    # Get `globals()` from the enviroment where the function is executed
    caller_globals = dict(
        inspect.getmembers(inspect.stack()[1][0]))["f_globals"]
    # Find imported modules in the global namespace
    imported_modules = set(imports(caller_globals.items()))
    # If running in the notebook, print IPython with the other notebook modules
    if 'jupyter_core' in sys.modules.keys() and 'IPython' in imported_modules:
        imported_modules.remove('IPython')
    # Include all modules from sys.modules
    if print_sys_modules:
        sys_modules = set(sys.modules.keys())
        imported_modules = imported_modules.union(sys_modules)
    # Keep module basename only. Filter duplicates and excluded modules.
    if print_private_modules:
        clean_modules = set(module.split('.')[0] for module in imported_modules
                            if module not in excludes)
    else:
        clean_modules = set(module.split('.')[0] for module in imported_modules
                            if module not in excludes
                            and not module.startswith('_'))
    # Find version number. Return NA if a version string can't be found.
    # This section is originally from `py_session` and modified slightly
    mod_and_ver = []
    for module in clean_modules:
        try:
            mod_and_ver.extend([
                f'{module:10}\t{sys.modules[module].__version__}'])
        except AttributeError:
            try:
                ver_type = type(sys.modules[module].version)
                if isinstance(ver_type, str) or isinstance(ver_type, int):
                    mod_and_ver.extend([
                        f'{module:10}\t{sys.modules[module].version}'])
                else:
                    mod_and_ver.extend([
                        f'{module:10}\t{sys.modules[module].version()}'])
            except AttributeError:
                try:
                    mod_and_ver.extend([
                        f'{module:10}\t{sys.modules[module].VERSION}'])
                except AttributeError:
                    if print_na:
                        mod_and_ver.extend([f'{module:10}\tNA'])
    mod_and_ver = sorted(mod_and_ver)
    print('\n'.join(mod_and_ver))
    # Print jupyter info separetely if running in the notebook
    if print_jupyter and 'jupyter_core' in sys.modules.keys():
        jup_modules = [sys.modules['IPython'], sys.modules['jupyter_client'],
                       sys.modules['jupyter_core']]
        try:
            import jupyterlab
            jup_modules.append(jupyterlab)
        except ModuleNotFoundError:
            pass
        try:
            import notebook
            jup_modules.append(notebook)
        except ModuleNotFoundError:
            pass
        jup_mod_and_ver = [f'{module.__name__:10}\t{module.__version__}'
                           for module in jup_modules]
        print('-----')
        print('\n'.join(jup_mod_and_ver))
    print('-----')
    print('Python ' + sys.version.replace('\n', ''))
    if print_os:
        print(platform.platform())
    print('-----')
    print('Session information updated at {}'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M')))
