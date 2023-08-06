# -*- coding: utf-8 -*-
import datetime
import os
import pkginfo
import sys
import time

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
pkg_info = pkginfo.Develop(os.path.join(os.path.dirname(__file__), '..'))
build_date = datetime.datetime.utcfromtimestamp(int(os.environ.get('SOURCE_DATE_EPOCH', time.time())))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
    ]

intersphinx_mapping = {
    'http://docs.python.org': None,
    'http://django.readthedocs.org/en/latest/': None,
    'http://sybil.readthedocs.io/en/latest/': None,
}

# General
source_suffix = '.txt'
master_doc = 'index'
project = pkg_info.name
copyright = '2008-2015 Simplistix Ltd, 2016-%s Chris Withers' % build_date.year
version = release = pkg_info.version
exclude_trees = ['_build']
exclude_patterns = ['description.txt']
pygments_style = 'sphinx'

# Options for HTML output
if on_rtd:
    html_theme = 'default'
else:
    html_theme = 'classic'
htmlhelp_basename = project+'doc'

# Options for LaTeX output
latex_documents = [
    ('index', project+'.tex', project+u' Documentation',
     'Simplistix Ltd', 'manual'),
]
