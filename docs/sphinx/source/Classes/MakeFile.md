# MakeFile Class

The MakeFile class acts as a representation of a single Makefile on the filesystem.
Typically you create one of these as a starting point and the other class's are created underneath automatically during the parsing of the Makefile

As a basic example
```python
from py_makefile_dbparse.makefile import MakeFile

# Read in the Makefile from the src directory underneath the current working directory
mk1 = MakeFile('src')

# Read in / parse the make database output
mk1.read_db()

# Parse everything from the database text
mk1.read_all()

# Expand a variable
expanded_var = mk1.vars.expand_var('OBJ')
```

## Class Description

```eval_rst

.. doxygenclass:: py_makefile_dbparse::makefile::MakeFile
  :members:

```
