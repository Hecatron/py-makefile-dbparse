'''
Configuration file for the Sphinx documentation builder.
https://www.sphinx-doc.org/en/master/usage/configuration.html
'''

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
sys.path.insert(0, os.path.abspath('../../../'))

import py_makefile_dbparse
from distutils.version import LooseVersion
from recommonmark.transform import AutoStructify

# -- Project information -----------------------------------------------------

project = 'py-makefile-dbparse'
html_title = 'py-makefile-dbparse'
release = LooseVersion(py_makefile_dbparse.__version__).vstring

copyright = '2019, Hecatrons Workshop'
author = 'Hecatrons Workshop'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'recommonmark',
    'sphinx_issues',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx_markdown_tables',
    'breathe'
]

issues_github_path = 'Hecatron/py-makefile-dbparse'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['Thumbs.db', '.DS_Store']

breathe_projects = {
    'py-makefile-dbparse':'../../doxygen/build/xml/'
}
breathe_default_project = 'py-makefile-dbparse'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = False
napoleon_use_keyword = True

# -- Options for HTML output -------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

language = 'en'
html_last_updated_fmt = ''
todo_include_todos = True
#html_favicon = 'images/favicon.ico'
html_use_index = True
html_domain_indices = True

# -- HTML theme settings ------------------------------------------------

# Theme settings file
#exec(open('./theme_material.py').read())
exec(open('./theme_bootstrap.py').read())
#exec(open('./theme_rtd.py').read())


# -- Plugin configuration ---------------------------------------------------

# Enable processing of markdown files
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

autosummary_generate = True
autoclass_content = 'class'

# Enable eval_rst in markdown
def setup(app):
    app.add_config_value(
        'recommonmark_config', {
		    'enable_math': True,
            'enable_inline_math': True,
            'enable_eval_rst': True,
            'enable_auto_toc_tree': False
        },
        True,
    )
    app.add_transform(AutoStructify)
