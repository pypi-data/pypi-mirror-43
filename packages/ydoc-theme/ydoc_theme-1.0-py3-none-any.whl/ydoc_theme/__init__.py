from os import path

__version__ = '1.0'
__version_full__ = __version__

def setup(app):
    app.add_html_theme('ydoc_theme', path.abspath(path.dirname(__file__)))

name = "ydoc_theme"