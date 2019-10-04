'''
Theme settings
'''

import sphinx_material

# Register the theme as an extension to generate a sitemap.xml
extensions.append('sphinx_material')

# Which theme to use
#html_theme = 'alabaster'
html_theme = 'sphinx_material'

# Get the them path
html_theme_path = sphinx_material.html_theme_path()
# Register the required helpers for the html context
html_context = sphinx_material.get_html_context()

# Theme options
html_theme_options = {

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    'base_url': 'https://Hecatron.github.io/py-makefile-dbparse',

    # Set the color and the accent color
    'color_primary': 'indigo',
    'color_accent': 'light-indigo',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/Hecatron/py-makefile-dbparse/',
    'repo_name': 'py-makefile-dbparse',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 2,
    # If False, expand all TOC entries
    'globaltoc_collapse': True,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,

    'html_minify': False,
    'html_prettify': True,
    'css_minify': True,
    'logo_icon': '&#xe869',

    'master_doc': False,

	# Navigation Links along the top bar
    'nav_links': [
        {'href': 'index', 'internal': True, 'title': 'Home'},
        {'href': 'https://www.hecatron.com/doku.php', 'internal': False, 'title': 'Blog'},
    ],
	# Titles that appear at the top of a given page
    'heroes': {
        'index': 'A library for extracting information from Makefiles using make.',
    },
}

html_show_sourcelink = True
html_sidebars = {
    '**': ['logo-text.html', 'globaltoc.html', 'localtoc.html', 'searchbox.html']
}
