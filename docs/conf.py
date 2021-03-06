# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../.'))

# -- Project information -----------------------------------------------------

project = 'Molecular Dynamics Project'
copyright = '2021, Anton Olsson, Daniel Stannelind, Daniel Spegel-Lexne, Martin Clason, Gustaf Åhlgren'
author = 'Anton Olsson, Daniel Stannelind, Daniel Spegel-Lexne, Martin Clason, Gustaf Åhlgren'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.napoleon","sphinx.ext.autodoc", "sphinx.ext.mathjax",
"sphinx.ext.viewcode", "sphinx.ext.githubpages", "sphinx.ext.intersphinx"
# ...
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_sidebars = { '**': ['globaltoc.html'] }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).

root_doc = 'index'
latex_documents = [
    (root_doc, 'ale_md.tex', u'ALE Molecular Dynamics Documentation',
     r'Anton Olsson \and Daniel Stannelind \and Daniel Spegel-Lexne \and Martin Clason \and Gustaf Åhlgren', 'manual'),
]

latex_elements = {
    'preamble' : r'''
%Make author names appear on separate lines
\DeclareRobustCommand{\and}{%
   \end{tabular}\kern-\tabcolsep\\\begin{tabular}[t]{c}%
}%

    '''
}
