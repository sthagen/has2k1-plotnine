# -*- coding: utf-8 -*-
#
# plotnine documentation build configuration file, created by
# sphinx-quickstart on Wed Dec 23 22:32:29 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

on_rtd = os.environ.get('READTHEDOCS') == 'True'
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(CUR_PATH + '/../')
sys.path.insert(0, CUR_PATH)
sys.path.insert(0, PROJECT_PATH)

if on_rtd:
    import mock
    from pprint import pprint
    MOCK_MODULES = []
    for mod_name in MOCK_MODULES:
        sys.modules[mod_name] = mock.Mock()
    pprint(os.environ)
    pprint(sys.path)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '3.0.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
sys.path.insert(0, os.path.abspath('.'))
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',

    'sphinxext.examples_and_gallery',
    'sphinxext.inline_code_highlight',

    'nbsphinx',
    'numpydoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'plotnine'
copyright = '2020, Hassan Kibirige'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.

try:
    import plotnine
    version = plotnine.__version__
except ImportError:
    version = 'unknown'

# readthedocs modifies the repository which messes up the version.
if on_rtd:
    import re
    version = version.rstrip('.dirty')
    version = re.sub(r'\+0\..+', '', version)
    version

# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    '_build',
    # Deprecated
    'generated/plotnine.themes.themeable.facet_spacing.rst'
]
# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# https://github.com/ryan-roemer/sphinx-bootstrap-theme
html_theme_options = {
    'navbar_title': 'plotnine',
    'globaltoc_depth': 2,
    'globaltoc_includehidden': 'true',
    'source_link_position': 'footer',
    'navbar_sidebarrel': False,
    'navbar_links': [
        ('API', 'api'),
        ('Gallery', 'gallery'),
        ('Tutorials', 'tutorials')
    ],
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['.']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'images/logo-32.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'images/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = {
    # Default to no sidebar
    '**': [],

    # local table of contents for the API page
    'api': ['localtoc.html']
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'plotninedoc'


# -- Options for LaTeX output ---------------------------------------------
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '12pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r"""
        \usepackage{charter}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}
    """,
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'plotnine.tex', 'plotnine Documentation',
   'Hassan Kibirige', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'plotnine', 'plotnine Documentation',
     ['Hassan Kibirige'], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'plotnine', 'plotnine Documentation',
   'Hassan Kibirige', 'plotnine', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False


# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = 'plotnine'
epub_author = 'Hassan Kibirige'
epub_publisher = 'Hassan Kibirige'
epub_copyright = '2020, Hassan Kibirige'

# The basename for the epub file. It defaults to the project name.
# epub_basename = 'plotnine'

# The HTML theme for the epub output. Since the default themes are not
# optimized for small screen space, using the same theme for HTML and epub
# output is usually not wise. This defaults to 'epub', a theme designed to
# save visual space.
# epub_theme = 'epub'

# The language of the text. It defaults to the language option
# or en if the language is not set.
# epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
# epub_scheme = ''

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
# epub_identifier = ''

# A unique identification for the text.
# epub_uid = ''

# A tuple containing the cover image and cover page html template filenames.
# epub_cover = ()

# A sequence of (type, uri, title) tuples for the guide element of content.opf.
# epub_guide = ()

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_pre_files = []

# HTML files shat should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_post_files = []

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# The depth of the table of contents in toc.ncx.
# epub_tocdepth = 3

# Allow duplicate toc entries.
# epub_tocdup = True

# Choose between 'default' and 'includehidden'.
# epub_tocscope = 'default'

# Fix unsupported image types using the PIL.
# epub_fix_images = False

# Scale large images.
# epub_max_image_width = 0

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# epub_show_urls = 'inline'

# If false, no index is generated.
# epub_use_index = True


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'statsmodels': ('https://www.statsmodels.org/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'sklearn': ('https://scikit-learn.org/stable/', None),
    'skmisc': ('https://has2k1.github.io/scikit-misc/stable/', None),
    'adjustText': ('https://adjusttext.readthedocs.io/en/latest/', None),
    'patsy': ('https://patsy.readthedocs.io/en/stable', None)
}

# -- Extension configuration ----------------------------------------------
autodoc_member_order = 'bysource'
autosummary_generate = True

extlinks = {
    'issue': ('https://github.com/has2k1/plotnine/issues/%s', 'GH')
}


# numpydoc
numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
numpydoc_xref_param_type = True
numpydoc_xref_aliases = {
    # python
    'sequence': ':term:`python:sequence`',
    'iterable': ':term:`python:iterable`',
    'string': 'str',
    'tuples': 'tuple',
    'boolean': 'bool',
    # numpy
    'array': 'numpy.ndarray',
    'np.array': 'numpy.ndarray',
    'ndarray': 'numpy.ndarray',
    'array-like': ':term:`array-like<numpy:array_like>`',
    'array_like': ':term:`numpy:array_like`',
    # pandas
    'dataframe': 'pandas.DataFrame',
    'DataFrame': 'pandas.DataFrame',
    'Series': 'pandas.Series',
    'series': 'pandas.Series',
    # plotnine
    'geom': ':term:`geom`',
    'stat': ':term:`stat`',
    'position': ':term:`position`',
    'expression': ':term:`expression`',
    'aes': 'plotnine.aes',
    'ggplot': 'plotnine.ggplot',
    'element_line': 'plotnine.themes.element_line',
    'element_rect': 'plotnine.themes.element_rect',
    'element_text': 'plotnine.themes.element_text',
}

numpydoc_xref_ignore = {'type', 'optional', 'default'}


def link_to_tutorials():
    # Linking to the directory does not work well with
    # nbsphinx. We link to the files themselves
    from glob import glob
    from plotnine_examples.tutorials import TUTPATH

    dest_dir = os.path.join(CUR_PATH, 'tutorials')

    # Unlink files from previous build
    for old_file in glob(dest_dir + '/*.ipynb'):
        os.unlink(old_file)

    # Link files for this build
    for file in glob(TUTPATH + '/*.ipynb'):
        basename = os.path.basename(file)
        dest = os.path.join(dest_dir, basename)
        os.symlink(file, dest)


def setup(app):
    link_to_tutorials()
    app.add_css_file('custom.css')
