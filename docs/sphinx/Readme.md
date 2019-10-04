# Readme

## Sphinx

Sphinx is a site generator that can read rst or markdown files to generate a static site. <br>
This can be published to a Git Repo's gh-pages branch.
Anything posted within a gh-pages branch on github is automatically visible as a static web site. <br>

## Script commands

The make.py file is a wrapper around the spinx build commands to add some additional functionality <br>
Additional commands include

  * **make.py clean** - Cleans the build directory
  * **make.py serve** - Serv / demo the site on http://127.0.0.1:8000
  * **make.py doxygen** - Do the build of the doxygen files
  * **make.py build** - Does a 'clean' then a 'buld'
  * **make.py publish** - Generate and publish a site to github.io (gh-pages branch) for the repo

The serve command is useful for demoing the site before pushing to github pages

## Building the documentation

### Entering the virtual python environment

First we need to setup a virtual python environment
```
cd virtenv
setup_venv.bat
```

This should install any needed dependencies from dev_requirements.txt and set everything up for building the docs

### Building doxygen xml files

Next we need to use doxygen to generate some xml files. <br>
Make sure doxygen is installed on the system

we can ether
```
cd docs/doxygen
doxygen
```
or
```
cd docs/sphinx
make.py doxygen
```

### Building the sphinx docs

To get a preview of what the docs will look like before they're posted to github pages. <br>
```
make.py serve
```

To just build a copy of the docs into the build directory
```
make.py build
```

### Publishing to github pages

To upload / publish a copy of the docs to the github pages branch
```
make.py publish
```

## Links

  * https://github.com/yoloseem/awesome-sphinxdoc
    General links to extensions / themes etc for sphinx
  * https://breathe.readthedocs.io/en/latest/
    This allows for the parsing of xml output from doxygen into sphnx docs
  * https://bashtage.github.io/sphinx-material/markdown.html
    Adding Markdown support to sphinx
  * https://github.com/bareos/bareos/tree/bareos-18.2
    An example of a nested table of contents within a page
  * https://github.com/sphinx-doc/sphinx/blob/master/sphinx/themes/basic/layout.html
    When writing custom themes, these are the pages inherited from as a base

### Documenting Code

  * https://github.com/Feneric/doxypypy/tree/master/doxypypy/test
  * https://jamwheeler.com/college-productivity/how-to-write-beautiful-code-documentation/
  * https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
