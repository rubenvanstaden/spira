import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon']
extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']

import sphinx_rtd_theme
from spira.settings import __version__, __release__

templates_path = ['_templates']
source_suffix = ['.rst', '.md']

master_doc = 'index'

project = u'SPiRA'
copyright = u'2019, Ruben van Staden'
author = u'Ruben van Staden'

version = __version__ 
release = __release__

language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = True
html_theme = 'sphinx_rtd_theme'

html_static_path = ['']

html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html',
    ]
}

htmlhelp_basename = 'spiradoc'

latex_elements = {}

latex_documents = [
    (master_doc, 'spira.tex', u'SPiRA Documentation',
     u'Ruben van Staden', 'manual'),
]

man_pages = [
    (master_doc, 'spira', u'SPiRA Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'spira', u'SPiRA Documentation',
     author, 'spira', 'One line description of project.',
     'Miscellaneous'),
]
