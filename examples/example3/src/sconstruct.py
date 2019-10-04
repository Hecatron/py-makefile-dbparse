import os
import sys
import SCons.Script
from SCons.Environment import Environment
from py_linq import Enumerable
from py_makefile_dbparse.makefile import MakeFile


# TODO Scons bug under windows?
def win_escape(x):
    if x[-1] == '\\':
        x = x + '\\'
    return x


tgts = []
EnsureSConsVersion(3, 1, 1)
env = Environment(ENV={'PATH': os.environ['PATH']})
if sys.platform == 'win32':
    env.AppendUnique(ENV={'SystemDrive': os.environ['SystemDrive']})
    env.AppendUnique(ENV={'TEMP': os.environ['TEMP']})

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

# TODO Scons bug under windows?
env['ESCAPE'] = win_escape

# Set our default targets to build when we don't specify anything at the command line
env.Default(tgts)
