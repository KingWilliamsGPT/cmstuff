'''Common stuff that I use that may not be yet implemented in python.

    I just use them as shortcut, and they speed of my debug workflow by 30%
'''

__author__ = ('Williams'
    '<williamusanga22@gmail.com>')

__version__ = '1.1'

__credits__ = '''Guido van Russom for creating such a beautiful language,
My mother for her understanding,
Simon for introducing me into programming.
And GOD for his infinite Love.'''

__all__ = [
'doc',
'classname',
# ----------------------
'mefun',
'methods',
'Stat',
'group',
'filterout',
'filterout_base_attrs',
'filterstr',
'from_import',
#----------------------
'cdesktop', 'pypath',
'desktop','HOME',
'cls', 'setargs', 'opendir', 'search_files',
#----------------------
'concat',
]

# from version 1.0 few changes have been made `exec` -> getattr,
# some functions have been removed or modified
# sys.exec_prefix if a new add on


import os
import sys
import io
import warnings
import subprocess
from os.path import join, expanduser, exists, dirname
from pprint import pprint
from types import ModuleType
from importlib import import_module

cls = lambda n=38:print('\n'*n)


def _isiterable(thing):
    'Checks if *thing is iterable'
    try:
        for i in thing:
            break
        return True
    except TypeError: # TypeError: 'thing' object is not iterable
        return False


def concat(stuff1, *stuffs, sep=' '):
    '''Just like printing with *print function except it returns the string right back
    
    takes items or a series of items (iterable) returns a
    string of space seperated item'''

    if not len(stuffs) and _isiterable(stuff1):
        stuffs = stuff1
    else:
        stuffs = [stuff1, *stuffs]
    s = sep.join([str(stuff) for stuff in stuffs])
    return s


def mend(fname, dir):
    return os.path.join(dir, fname)


def search_files(fname, recursive=True, dir='.', strict=False):
    """This Searches files in a directory recursively [if specified] searching
    if a keyword exists in the filenames. Usefull if you are searching for a
    file and you have an idea of the name and you know where it is.
    """
    dir = os.path.abspath(dir)
    if not strict: fname = fname.lower()
    if not recursive:
        return os.listdir(dir)
    for cd, _, files in os.walk(dir):
        for file in files:
            filepath = mend(file, cd)
            if not strict: file = file.lower()
            if fname in file:
                yield (fname, filepath)
        

##for file, path in search_files('data', True, r"C:\Users\williams\Documents\Books\New folder\python books"):
##	print(file, ':', path)
##	print()

def doc(obj, pr=True):
    """Get the documentation from an object if any.

    *pr* Decide whether to print it or return it defaults to print
    """
    doc_ = obj.__doc__
    if pr:
        print(obj.__doc__)
    else:
        return '' if doc_ is None else doc_


def classname(obj, suppress_errors=True):
    """Returns the classname of *obj*"""
    try:
        return obj.__class__.__name__
    except Exception as ex: # any arbitrary error could occur here
        if suppress_errors:
            pass
        else:
            raise Exception("could not complete the task") from ex




def _ismagic(attr):
    """Returns True if the *attr* is a magic method."""
    # works like magic. :)
    #if attr.startswith('__') and attr.endswith('__'): # this returns True for '__'
    if attr.startswith('__') and attr[2:].endswith('__'):
        return True
    else:
        return False

def _filter_magic(sequence):
    return [i for i in sequence if i[:1] != '_']


def mefun(obj):
    """Returns all callables except classes.
    Callable non classes."""

    result = []
    for strattrib in dir(obj):
        attrib = getattr(obj, strattrib) #eval('obj.' + strattrib) does'nt work for builtins.True
        if callable(attrib) and classname(attrib) != 'type' and not _ismagic(strattrib):
            result.append(strattrib)
    return _filter_magic(result)


def methods(obj):
    """Returns a list of methods excluding magic methods '__method__'."""
    # in the future methods will also optionaly give report on attrib that
    # aren'nt valid and why
    methods_ = []
    for attrib in dir(obj):
        #type = classname(eval('obj.' + attrib))
        type = classname(getattr(obj, attrib))
        
        if type in ('method', 'function','builtin_function_or_method'):
            if not _ismagic(attrib):
                methods_.append(attrib)
    else:
        return methods_


def group(obj):
    """Return a mapping for types to their respective attribs in *obj*.

    Just like Stat except the dict object is all yours."""
    
    category = {
        #type: [attribs, ...]
    }
    for attrib in dir(obj):
        type = classname(getattr(obj, attrib))
        if type not in category:
            category[type] = [attrib] # start list with non existing type
        else:
            category[type].append(attrib) # it exist add more
    return category
        
 
class Stat:
    """Group all types in a given object."""
    # a method stat.lookup(attrib) will be added to get all info about an attrib
    
    def __init__(self, object_):
        self.object = object_
        self.status = group(object_)
    
    def show(self, return_string=False, write_to=sys.stdout):
        """Pretify Stat.status."""
        if return_string:
            write_to = io.StringIO()
        print(str(self.object), file=write_to) # head
        for type, values in self.status.items():
            print(f'\n{type} ({len(values)}):\n', file=write_to)
            pprint(values, stream=write_to)
            print('-'*80, file=write_to)
        if return_string:
            write_to.seek(0)
            txt = write_to.read()
            return txt
    
    def types(self):
        """Returns a list of types."""
        return list(self.status.keys())

    def get(self, type):
        """Returns a list of attribs of the type *type*."""
        return self.status.get(type, None)



def filterout(type_, obj):
    """Returns list of specied types of an object *filterout('type'|type, object)*.

    like the get method in Stat."""
    # in the future you can add a list of types
    
    if not isinstance(type_, (str, type)):
        raise ValueError('type must be of type str or type not %s' % classname(type_))

    is_string = isinstance(type_, str)
    if is_string:
        return _filter_magic(
            [attr for attr in dir(obj) if classname(getattr(obj, attr)) == type_])
    else:
        return _filter_magic(
            [attr for attr in dir(obj) if isinstance(getattr(obj, attr), type_)])


def _getmod(module):
    # try to import a module *modname* could be a string or a module
    if isinstance(module, str):
        try:
            # exec(f'import {module}') # module only imported in string scope
            module = import_module(module)
            return module
        except ImportError as ex:
            raise ImportError(f"Could'nt import {module}") from ex
    
    elif type(module) == ModuleType:
        return module
    
    elif not isinstance(module, ModuleType):
        raise ValueError(
            'Invalid Type must be str or ModuleType got %s' % classname(module))


def from_import(modname, types='all', with_privates=False):
    """Import everything from a modules that might not be included in __all__."""
    
    module = _getmod(modname)
    assert module is not None
    
    # This is how I will add objects from `module` to your scope
    append = lambda mod_cut:\
             globals().update(
        {attr: getattr(module, attr) for attr in mod_cut}
        )
    
    all = dir(module)
    all = all if types == 'all' else filterout(types, module)
    if not with_privates: all = [i for i in all if i[:1] != '_']
    append(all)
    return all
    


def filterstr(s, object, ignore_privates=True):
    "Filterout attributes containing *s*"
    ret = []
    for i in dir(object):
        if i.startswith('_') and ignore_privates:
            continue
        if s in i:
            ret.append(i)
    return ret
# -----------------------------------------------------------------------------------
# path related

HOME = expanduser('~')
desktop = lambda: join(HOME, 'desktop')

def pypath():
    """Returns abspath to python home."""
    try:
        from os import __file__
        return dirname(dirname(__file__))
    except ImportError:
        return sys.exec_prefix


def cdesktop():
    """Change directory to the desktop.
    
    Normally people like to work on there desktop this could come pretty much in
    handy. :)
    """
    #homepath = join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH']) or os['HOME']

    def dir_failure():
        if os.getcwd() == pypath():
            warnings.warn('desktop may have not been found', RuntimeWarning)
    
    if sys.platform.lower().startswith('win'):
        try:    # windows sweet
            os.chdir(desktop())
        except FileNotFoundError as ex:
            raise Exception("Could'nt change to desktop on windows") from ex
        finally:
            dir_failure()
            return os.getcwd()
    else:   # quirk mode
        for folder in os.listdir(HOME):
            if folder.lower() == 'desktop':
                os.chdir(join(HOME, folder))
                return os.getcwd()
        else:
            raise FileNotFoundError('On {platform} but could not find desktop'.format(
                platform = sys.platform))


def setargs(arg, *args):
    '''Set `sys.argv`
            Probably an easier way to set arguments to `sys.args` other than `sys.argv = [a, b, c]`.
            If sys.argv[0] is not specied (first argument is not __name__) it will be inserted
            USE:
                    > setargs('a b c d e f')
                    > setargs('a', 'b', 'c d')
                    > setargs(__name__,' a b c d')
                    
            args:
                    `arg` could be a string like `a` or `a b c`
                    `args` list of string
                    
            returns:
                    sys.argv
    '''
    getArgs = lambda obj: str(obj).strip().split(' ')
    arguments = []
    arguments.extend(getArgs(arg))
    import os.path as path
    if arg:
        for i in args:
            arguments.extend(getArgs(i))
    if arguments:
        # add File name if not specified
        thisFile = path.basename(__name__)
        if not thisFile in arguments[0]:
            arguments.insert(0, thisFile)
    sys.argv = arguments
    return (sys.argv or arguments)


def opendir(dir=None):
    '''opens a directory Python's by default'''
    dir = dir or sys.base_exec_prefix
    former_dir = os.getcwd()
    os.chdir(dir)
    subprocess.call('start .', shell=True)
    os.chdir(former_dir) # change dir back to user's dir


def _union(*sets):
    '''Returns a universal set where all *sets provided are subset'''
    # in english terms it just unifies all sets (set1, set2) and returns it
    mama = set()
    for set_ in sets:
        mama = mama.union(set_)
    return mama


def filterout_base_attrs(object):
    '''Returns a list of all properties of *object* except those inherited.'''
    base_classes = object.__class__.__mro__[1:]
    base_attrs = _union(*[set(dir(klass)) for klass in base_classes])
    all_attrs = set(dir(object))
    return list(all_attrs - base_attrs)

fibar = filterout_base_attrs # FIlterout Base AttRs
__all__.append('fibar')