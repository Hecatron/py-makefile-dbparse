import os
import sys
import SCons.Script
from SCons.Environment import Environment


# Todo scons issue?
def win_escape(x):
    if x[-1] == '\\':
        x = x + '\\'
    return x


EnsureSConsVersion(3, 1, 1)

# One way is to import everything into the construction env from the environment
#env = Environment(ENV=os.environ)

# Another way is to just import the path
# Note For windows we also need temporary paths adding in for windows build tools
env = Environment(ENV={'PATH': os.environ['PATH']})
if sys.platform == 'win32':
    env.AppendUnique(ENV={'SystemDrive': os.environ['SystemDrive']})
    env.AppendUnique(ENV={'TEMP': os.environ['TEMP']})


env.Replace(BUILDDIR='../build')
env.Replace(SRCDIR='.')
env.Replace(CPPPATH='./include')

tgts = []

# Create Objects
scons_obj1 = env.Object(target='${BUILDDIR}/hellomake', source='${SRCDIR}/hellomake')
scons_obj2 = env.Object(target='${BUILDDIR}/hellofunc', source='${SRCDIR}/hellofunc')

# Link the objects to an exe
scons_prog = env.Program(target='${BUILDDIR}/hellomake', source=['${BUILDDIR}/hellomake', '${BUILDDIR}/hellofunc'])

# This probably isn't needed since scons scans the source for dependencies but just in case
# Add a dependency here for the main program against the objects
env.Requires(scons_prog, [scons_obj1, scons_obj2])

tgts += [scons_prog, scons_obj1, scons_obj2]

env['ESCAPE'] = win_escape
env.Default(tgts)
