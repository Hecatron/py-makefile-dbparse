# py-makefile-dbparse

A tool for extracting information from Makefiles for use with build systems such as scons. <br>
make is used to extract the Makefile database information without actually building any sources

The original reason I wrote this was to try and partially port some C sources across from Makefiles to Scons
without having to port all the Makefiles all at once.
So make is effectively passing on some of it's information onto python which can then use scons to handle the building.
(one example of where this can help is when your trying to build something under windows instead of linux)

## How it works

The way this library typically works is to run an installed copy of **make** against a given Makefile within a directory structure. <br>
The option used is typically "-pn" which dumps the make database to stdout, this library then attempts to parse this output to extract information such as

  * Make variables such as lists of sources or object files
  * Targets to be built
  * Dependencies for targets
  * Compile options for targets

There's also the option to:

  * Read an existing Makefile into memory
  * Add on a target / rule to the Makefile in memory to output the result of a specific variable or set of variables
  * This handles situations where the variable may contain modifiers / make functions (such as subst)
  * Then run the altered Makefile in memory using make to output and capture the information (without building the sources)

## Development

To develop or try out the examples

```
cd virtenv
# windows
setup_venv.bat
# Linux
setup_venv.sh
```

Then open **py-makefile-dbparse.code-workspace** within Visual Studio Code


## Simiar Projects

The idea for this was based on another library called make_var

  * [make-var](https://github.com/karnigen/make_var)

There's also some other libraries that provide similar information

  * [py-make](https://github.com/tqdm/py-make)
  * [compiledb](https://pypi.org/project/compiledb/)

I've discovered that py-make seems to have limits on the compatibility with existing Makefiles
and compiledb doesn't show all the information I need, but does provide some interesting infromation.

With this library I'm actually using make to extract the build information as part of a gradual porting process to a different build system.
This makes parsing the makefiles a bit easier

```eval_rst
.. toctree::
   :name: mastertoc

   /Classes/index.rst
   /Examples/index.rst
```
