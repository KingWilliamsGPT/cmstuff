# Overview of cmstuff:

The code provides a set of commonly used functions and shortcuts to make coding in Python easier. It includes shortcuts for printing, file searching, directory management, and more.

The code begins with a set of metadata that includes the author, version, and credits. The `__all__` variable lists all of the functions that are available to import from this module.

The first few functions are basic utilities that are used in other parts of the code. The `_isiterable` function checks if an object is iterable. The `concat` function takes in any number of arguments and concatenates them together, returning a string. The `mend` function takes in a filename and directory name and returns the full file path. The `search_files` function searches for a file within a directory and returns a generator object with the filenames and paths.

The `doc` function takes in an object and prints out its documentation. The `classname` function takes in an object and returns its class name. The `mefun` function takes in an object and returns all of its callable non-class attributes. The `methods` function takes in an object and returns a list of its methods, excluding magic methods. The `group` function takes in an object and returns a mapping for types to their respective attributes in the object.

The last set of functions provide shortcuts for common tasks. `cdesktop` returns the path to the desktop directory. `pypath` returns the path to the Python installation directory. `desktop` returns the path to the user's desktop directory. `HOME` and `WORK_AREA` return the path to the user's home and work directories, respectively. `cls` clears the console output. `setargs` takes in a list of arguments and returns them as a dictionary. `opendir` opens a directory in the operating system's file explorer.



## Example


Function: `filterstr`
This function takes in three parameters:

`s` - a string to filter out attributes containing this value
object - the object to be filtered
`ignore_privates` - a boolean value indicating whether private attributes (those starting with an underscore) should be ignored (default is True)
The function iterates through the attributes of the object and filters out those that contain the s value. It returns a list of the filtered attributes.

Parameters
`s` (required) - a string to filter out attributes containing this value
`object` (required) - the object to be filtered
`ignore_privates` (optional) - a boolean value indicating whether private attributes (those starting with an underscore) should be ignored (default is True)
Return Value
`ret` - a list of the filtered attributes

**Example Usage**


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

# try to filter the methods and attributes that are relevant to you
filtered_attrs = cm.filterstr("name", example)

# it returns an array so you can do further processing
print(filtered_attrs)  # Output: ['full_name', 'name', 'other_name']


# If you think this is cool try 
# cm.Stat(example).show()
```


## Author
  You can check out my email at williamusanga22@gmail.com :smiley:


