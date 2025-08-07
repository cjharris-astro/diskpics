# Configuration file for the Sphinx documentation builder.

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(basepath)
print(basepath)
print(basepath)
print(basepath)
print(basepath)
print(basepath)
print(basepath)
print(basepath)
#raise Exception(ValueError)
sys.path.insert(0, basepath)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'diskpics'
copyright = '2025, noura,CJ,Marbely'
author = 'noura,CJ,Marbely'
root_doc = 'index'
release = 'v0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc","sphinx.ext.napoleon","sphinx.ext.autosummary","sphinx.ext.viewcode"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'english'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
