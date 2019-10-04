# MakeLauncher Class

The MakeLauncher class acts as a wrapper around subprocess to launch the make executable. <br>
To give an example of extracting the make database in the current directory.

```python
from py_makefile_dbparse.launcher import MakeLauncher

mklaunch = MakeLauncher(workdir='./')
dbtxt = mklaunch.run('-pn')
```

## Class Description

```eval_rst

.. doxygenclass:: py_makefile_dbparse::launcher::MakeLauncher
  :members:

```
