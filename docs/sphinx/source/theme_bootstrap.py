'''
Theme settings
'''

import sphinxbootstrap4theme

html_theme = 'sphinxbootstrap4theme'
html_theme_path = [sphinxbootstrap4theme.get_path()]
#html_theme_path = ['D://SourceCode//GitRepos.Forks//sphinxbootstrap4theme//themes']

# Html logo in navbar.
# Fit in the navbar at the height of image is 37 px.
#html_logo = '_static/logo.jpg'

html_theme_options = {
    # Navbar style.
    # Values: 'fixed-top', 'full' (Default: 'fixed-top')
    'navbar_style' : 'fixed-top',

    # Navbar link color modifier class.
    # Values: 'dark', 'light' (Default: 'dark')
    #'navbar_color_class' : 'light',

    # Navbar background color class.
    # Values: 'inverse', 'primary', 'faded', 'success',
    #         'info', 'warning', 'danger' (Default: 'inverse')
    #'navbar_bg_class' : 'info',

    # Show global TOC in navbar.
    # To display up to 4 tier in the drop-down menu.
    # Values: True, False (Default: True)
    #'navbar_show_pages' : True,

    # Link name for global TOC in navbar.
    # (Default: 'Pages')
    #'navbar_pages_title' : 'Pages',

    # Specify a list of menu in navbar.
    # Tuples forms:
    #  ('Name', 'external url or path of pages in the document', boolean)
    # Third argument:
    # True indicates an external link.
    # False indicates path of pages in the document.
    'navbar_links' : [
         ('Github', 'https://github.com/Hecatron/py-makefile-dbparse', True),
         ("Page Index", "genindex", False),
         ("Blog", "https://www.hecatron.com/doku.php", True),
    ],

    # Total width(%) of the document and the sidebar.
    # (Default: 80%)
    #'main_width' : '80%',

    # Render sidebar.
    # Values: True, False (Default: True)
    #'show_sidebar' : True,

    # Render sidebar in the right of the document.
    # Values: True, False (Default: True)
    'sidebar_right': False,

    # Fix sidebar.
    # Values: True, False (Default: True)
    'sidebar_fixed': True,

    # Html table header class.
    # Values: 'inverse', 'light' (Default: 'inverse')
    #'table_thead_class' : 'light',

    # Bootswatch color theme
	# (Default: 'None')
    'bootswatch': 'flatly',

    #'extra_nav_links': {'Page index':'/genindex.html'},
}

# Pygments color theme for code
#pygments_style = 'monokai'
#pygments_style = 'solarized-dark'

html_css_files = [
    'css/custom.css',
    'css/customtoc_bootstrap.css'
]

html_sidebars = {
    '**': ['globaltoc.html','localtoc.html','customtoc_bootstrap.html', 'searchbox.html']
}
