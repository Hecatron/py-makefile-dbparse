# SCons Example

One example is that we can use this library to extract information from a Makefile
and then pass it onto scons to handle the build.

On it's own the below probably wouldn't make that much sense since you'd be better off just rewritting the below purely for scons.
But in the case of a much more complex build involving existing Makefiles it would make the porting process a bit easier
if you were moving to something like Meson or Scons as a build system but didn't want to move everything across all at once.

```python
import os
import sys
import SCons.Script
from SCons.Environment import Environment
from py_linq import Enumerable
from py_makefile_dbparse.makefile import MakeFile

# Lets setup a construction environment
tgts = []
EnsureSConsVersion(3, 1, 1)
env = Environment(ENV={'PATH': os.environ['PATH']})
if sys.platform == 'win32':
    env.AppendUnique(ENV={'SystemDrive': os.environ['SystemDrive']})
    env.AppendUnique(ENV={'TEMP': os.environ['TEMP']})

# Lets read in the Makefile database
mk1 = MakeFile('.')
mk1.read_all()
# Lets wrap the list of targets in a Enumerable so we can use py_linq on it
make_targets = Enumerable(mk1.targets)

# Find the main program in the list of targets
make_prog = make_targets.where(lambda x: x.target == '../build/hellomake').first_or_default()
# Register the program with scons
scons_prog = env.Program(target=make_prog.target_noext, source=make_prog.sources)
# Add scons program to list of targets we want to build
tgts.append(scons_prog)

# Next lets find any target ending with .o
make_deps = make_targets.where(lambda x: x.target.endswith('.o'))

for dep_item in make_deps:
    # Create a Scons Object target for the item we've found ending in .o
    scons_obj = env.Object(target=dep_item.target, source=dep_item.sources_noheader)
    # Add to the list of things we want to build
    tgts.append(scons_obj)
    # This probably isn't needed since scons scans the source for dependencies but just in case
    # Add a dependency here for the main program against the objects
    env.Requires(scons_prog, scons_obj)

env.Replace(CFLAGS=mk1.vars.expand_var('CFLAGS'))

# Set our default targets to build when we don't specify anything at the command line
env.Default(tgts)
```
