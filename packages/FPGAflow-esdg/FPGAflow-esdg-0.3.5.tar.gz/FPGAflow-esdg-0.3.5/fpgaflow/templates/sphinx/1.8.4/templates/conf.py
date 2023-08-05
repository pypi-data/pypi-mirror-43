extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'releases',
    'breathe',
]

templates_path = ['_templates']
source_suffix = ['.rst', '.md']
language = None
exclude_patterns = []
pygments_style = 'rainbow_dash'
html_theme = 'sphinx_rtd_theme'

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

epub_title = project
epub_exclude_files = ['search.html']
todo_include_todos = True
