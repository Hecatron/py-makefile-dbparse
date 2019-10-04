'''
Theme settings
'''

# Register the theme as an extension to generate a sitemap.xml
extensions.append('sphinx_rtd_theme')

html_theme = "sphinx_rtd_theme"

html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}
