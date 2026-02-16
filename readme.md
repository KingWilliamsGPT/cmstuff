# cmstuff

Common Python shortcuts and utilities that speed up debug workflows by 30%.

## Installation

```bash
pip install cmstuff
```

For development:

```bash
git clone https://github.com/Williams/cmstuff.git
cd cmstuff
pip install -e .
```

## Overview

The library provides a set of commonly used functions and shortcuts to make coding in Python easier. It includes shortcuts for printing, file searching, directory management, introspection, and logging.

### Introspection utilities

- `doc(obj)` — print or return documentation from an object
- `classname(obj)` — return the class name of an object
- `mefun(obj)` — return all callable non-class attributes
- `methods(obj)` — return a list of methods (excluding magic methods)
- `group(obj)` — return a mapping of types to their respective attributes
- `Stat(obj)` — group and display all types in an object
- `filterout(type_, obj)` — filter attributes by type
- `filterout_base_attrs(obj)` — list properties not inherited from base classes
- `filterstr(s, obj)` — filter attributes containing a substring

### Path utilities

- `HOME` — path to user home directory
- `desktop()` — path to the desktop
- `cdesktop()` — change working directory to the desktop
- `pypath()` — path to the Python installation
- `opendir(dir)` — open a directory in the file explorer
- `search_files(fname)` — recursively search for files by keyword

### Other utilities

- `concat(*items)` — concatenate items into a space-separated string
- `cls()` — clear the console
- `setargs(arg, *args)` — set `sys.argv` conveniently
- `get_logger(...)` — create a custom logger with sensible defaults
- `get_caller_module()` — get the module of the calling code

## Example

```python
import cmstuff as cm


class Example:
    def __init__(self):
        self.name = "John"
        self.age = 30
        self._id = "12345"
        self.other_name = "Doodleman"

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")

    def full_name(self):
        return f"{self.name} {self.other_name}"


# get an object
example = Example()

# filter the methods and attributes that are relevant to you
filtered_attrs = cm.filterstr("name", example)

# it returns a list so you can do further processing
print(filtered_attrs)  # Output: ['full_name', 'name', 'other_name']

# If you think this is cool try
# cm.Stat(example).show()
```

## Author

Williams — williamusanga22@gmail.com

## License

MIT


