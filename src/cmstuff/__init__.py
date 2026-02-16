"""Common stuff that I use that may not be yet implemented in python.

I just use them as shortcut, and they speed of my debug workflow by 30%
"""

__author__ = 'Williams <williamusanga22@gmail.com>'

__version__ = '1.1.0'

__credits__ = '''Guido van Russom for creating such a beautiful language,
My mother for her understanding,
Simon for introducing me into programming.
And GOD for his infinite Love.'''

__all__ = [
    # introspection
    'doc',
    'classname',
    'mefun',
    'methods',
    'group',
    'Stat',
    'filterout',
    'filterout_base_attrs',
    'fibar',
    'filterstr',
    'from_import',
    # utilities
    'cls',
    'concat',
    'setargs',
    'search_files',
]


import os
import sys
import io
from pprint import pprint
from types import ModuleType
from importlib import import_module


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

cls = lambda n=38: print('\n' * n)


def _isiterable(thing):
    """Check if *thing* is iterable."""
    try:
        iter(thing)
        return True
    except TypeError:
        return False


def concat(stuff1, *stuffs, sep=' '):
    '''Just like printing with *print function except it returns the string right back

    takes items or a series of items (iterable) returns a
    string of space seperated item'''

    if not len(stuffs) and _isiterable(stuff1):
        stuffs = stuff1
    else:
        stuffs = [stuff1, *stuffs]
    return sep.join(str(stuff) for stuff in stuffs)


def setargs(arg, *args):
    '''Set `sys.argv`

    Probably an easier way to set arguments to `sys.args` other than
    ``sys.argv = [a, b, c]``.  If ``sys.argv[0]`` is not specified
    (first argument is not ``__name__``) it will be inserted.

    Usage::

        setargs('a b c d e f')
        setargs('a', 'b', 'c d')
        setargs(__name__, 'a b c d')
    '''
    getArgs = lambda obj: str(obj).strip().split(' ')
    arguments = []
    arguments.extend(getArgs(arg))
    if arg:
        for i in args:
            arguments.extend(getArgs(i))
    if arguments:
        thisFile = os.path.basename(__name__)
        if thisFile not in arguments[0]:
            arguments.insert(0, thisFile)
    sys.argv = arguments
    return sys.argv or arguments


# ---------------------------------------------------------------------------
# File search
# ---------------------------------------------------------------------------

def search_files(fname, recursive=True, dir='.', strict=False):
    """Search files in a directory recursively (if specified), checking
    if a keyword exists in the filenames.

    Useful if you are searching for a file and you have an idea of the
    name and you know where it is.
    """
    dir = os.path.abspath(dir)
    if not strict:
        fname = fname.lower()
    if not recursive:
        return os.listdir(dir)
    for cd, _, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(cd, file)
            if not strict:
                file = file.lower()
            if fname in file:
                yield (fname, filepath)


# ---------------------------------------------------------------------------
# Introspection helpers
# ---------------------------------------------------------------------------

def doc(obj, pr=True):
    """Get the documentation from an object if any.

    *pr* — decide whether to print it or return it (defaults to print).
    """
    doc_ = obj.__doc__
    if pr:
        print(doc_)
    else:
        return '' if doc_ is None else doc_


def classname(obj, suppress_errors=True):
    """Return the class name of *obj*."""
    try:
        return obj.__class__.__name__
    except Exception as ex:
        if suppress_errors:
            return None
        raise Exception("could not complete the task") from ex


def _ismagic(attr):
    """Return True if *attr* is a dunder name."""
    return attr.startswith('__') and attr[2:].endswith('__')


def _filter_private(sequence):
    """Remove names starting with ``_``."""
    return [i for i in sequence if not i.startswith('_')]


def mefun(obj):
    """Return all callable non-class attributes (excluding magic methods)."""
    result = []
    for name in dir(obj):
        attr = getattr(obj, name)
        if callable(attr) and classname(attr) != 'type' and not _ismagic(name):
            result.append(name)
    return _filter_private(result)


def methods(obj):
    """Return a list of methods excluding magic methods."""
    result = []
    for name in dir(obj):
        typename = classname(getattr(obj, name))
        if typename in ('method', 'function', 'builtin_function_or_method'):
            if not _ismagic(name):
                result.append(name)
    return result


def group(obj):
    """Return a mapping of type-names to their respective attribute names in *obj*.

    Just like ``Stat`` except the dict object is all yours.
    """
    category = {}
    for name in dir(obj):
        typename = classname(getattr(obj, name))
        category.setdefault(typename, []).append(name)
    return category


class Stat:
    """Group all types in a given object."""

    def __init__(self, object_):
        self.object = object_
        self.status = group(object_)

    def show(self, return_string=False, write_to=sys.stdout):
        """Pretty-print ``Stat.status``."""
        if return_string:
            write_to = io.StringIO()
        print(str(self.object), file=write_to)
        for typename, values in self.status.items():
            print(f'\n{typename} ({len(values)}):\n', file=write_to)
            pprint(values, stream=write_to)
            print('-' * 80, file=write_to)
        if return_string:
            write_to.seek(0)
            return write_to.read()

    def types(self):
        """Return a list of type-names."""
        return list(self.status.keys())

    def get(self, typename):
        """Return a list of attributes of type *typename*."""
        return self.status.get(typename, None)


def filterout(type_, obj):
    """Return public attributes of *obj* whose type matches *type_*.

    *type_* can be a type name string or an actual ``type``.
    """
    if not isinstance(type_, (str, type)):
        raise ValueError(
            'type_ must be str or type, not %s' % classname(type_))

    if isinstance(type_, str):
        return _filter_private(
            [a for a in dir(obj) if classname(getattr(obj, a)) == type_])
    return _filter_private(
        [a for a in dir(obj) if isinstance(getattr(obj, a), type_)])


def filterstr(s, object, ignore_privates=True):
    """Filter attributes of *object* whose name contains *s*."""
    ret = []
    for name in dir(object):
        if name.startswith('_') and ignore_privates:
            continue
        if s in name:
            ret.append(name)
    return ret


def filterout_base_attrs(object):
    """Return attributes of *object* that are NOT inherited from base classes."""
    base_classes = object.__class__.__mro__[1:]
    base_attrs = set().union(*(set(dir(klass)) for klass in base_classes))
    return list(set(dir(object)) - base_attrs)


fibar = filterout_base_attrs  # shorthand alias


# ---------------------------------------------------------------------------
# Module importing
# ---------------------------------------------------------------------------

def _getmod(module):
    """Resolve *module* (str or ModuleType) to a module object."""
    if isinstance(module, str):
        try:
            return import_module(module)
        except ImportError as ex:
            raise ImportError(f"Couldn't import {module}") from ex
    if isinstance(module, ModuleType):
        return module
    raise ValueError(
        'Expected str or ModuleType, got %s' % classname(module))


def from_import(modname, types='all', with_privates=False):
    """Import everything from a module that might not be included in ``__all__``."""
    module = _getmod(modname)
    assert module is not None

    attrs = dir(module)
    if types != 'all':
        attrs = filterout(types, module)
    if not with_privates:
        attrs = [i for i in attrs if not i.startswith('_')]

    globals().update({attr: getattr(module, attr) for attr in attrs})
    return attrs