# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = 'Sparky Buddy Training'
copyright = '2023, KHM Smart Build'
author = 'KHM Smart Build'
release = '0.0.01'

# -- General configuration ---------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('..'))  # update this to the path of your Python files

extensions = [
    'sphinx.ext.autodoc',  # Support for docstrings
    'sphinx.ext.napoleon',  # Support for NumPy and Google style docstrings
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
