# -*- coding: utf-8 -*-
import sys
import os
import alabaster
from pyquickhelper.helpgen.default_conf import set_sphinx_variables

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
local_template = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "phdoc_templates")

set_sphinx_variables(__file__, "mathenjeu", "Xavier Dupré", 2021,
                     "alabaster", alabaster.get_path(),
                     locals(), extlinks=dict(
                         issue=('https://github.com/sdpython/mathenjeu/issues/%s', 'issue')),
                     title="Exercices via une application web", book=True, nblayout='table')

blog_root = "http://www.xavierdupre.fr/app/mathenjeu/helpsphinx/"
extensions.append("sphinxcontrib.blockdiag")
# blockdiag_fontpath = '/usr/share/fonts/truetype/ipafont/ipagp.ttf'

html_css_files = ['my-styles.css']

html_logo = "project_ico.png"

language = "fr"

preamble = '''
\\usepackage{etex}
\\usepackage{fixltx2e} % LaTeX patches, \\textsubscript
\\usepackage{cmap} % fix search and cut-and-paste in Acrobat
\\usepackage[raccourcis]{fast-diagram}
\\usepackage{titlesec}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{amsfonts}
\\usepackage{graphics}
\\usepackage{epic}
\\usepackage{eepic}
%\\usepackage{pict2e}
%%% Redefined titleformat
\\setlength{\\parindent}{0cm}
\\setlength{\\parskip}{1ex plus 0.5ex minus 0.2ex}
\\newcommand{\\hsp}{\\hspace{20pt}}
\\newcommand{\\acc}[1]{\\left\\{#1\\right\\}}
\\newcommand{\\cro}[1]{\\left[#1\\right]}
\\newcommand{\\pa}[1]{\\left(#1\\right)}
\\newcommand{\\R}{\\mathbb{R}}
\\newcommand{\\HRule}{\\rule{\\linewidth}{0.5mm}}
%\\titleformat{\\chapter}[hang]{\\Huge\\bfseries\\sffamily}{\\thechapter\\hsp}{0pt}{\\Huge\\bfseries\\sffamily}
'''

custom_preamble = """\n
\\usepackage[all]{xy}
\\newcommand{\\vecteur}[2]{\\pa{#1,\\dots,#2}}
\\newcommand{\\N}[0]{\\mathbb{N}}
\\newcommand{\\indicatrice}[1]{\\mathbf{1\\!\\!1}_{\\acc{#1}}}
\\newcommand{\\infegal}[0]{\\leqslant}
\\newcommand{\\supegal}[0]{\\geqslant}
\\newcommand{\\ensemble}[2]{\\acc{#1,\\dots,#2}}
\\newcommand{\\fleche}[1]{\\overrightarrow{ #1 }}
\\newcommand{\\intervalle}[2]{\\left\\{#1,\\cdots,#2\\right\\}}
\\newcommand{\\loinormale}[2]{{\\cal N}\\pa{#1,#2}}
\\newcommand{\\independant}[0]{\\;\\makebox[3ex]{\\makebox[0ex]{\\rule[-0.2ex]{3ex}{.1ex}}\\!\\!\\!\\!\\makebox[.5ex][l]{\\rule[-.2ex]{.1ex}{2ex}}\\makebox[.5ex][l]{\\rule[-.2ex]{.1ex}{2ex}}} \\,\\,}
\\newcommand{\\esp}{\\mathbb{E}}
\\newcommand{\\var}{\\mathbb{V}}
\\newcommand{\\pr}[1]{\\mathbb{P}\\pa{#1}}
\\newcommand{\\loi}[0]{{\\cal L}}
\\newcommand{\\vecteurno}[2]{#1,\\dots,#2}
\\newcommand{\\norm}[1]{\\left\\Vert#1\\right\\Vert}
\\newcommand{\\norme}[1]{\\left\\Vert#1\\right\\Vert}
\\newcommand{\\dans}[0]{\\rightarrow}
\\newcommand{\\partialfrac}[2]{\\frac{\\partial #1}{\\partial #2}}
\\newcommand{\\partialdfrac}[2]{\\dfrac{\\partial #1}{\\partial #2}}
\\newcommand{\\loimultinomiale}[1]{{\\cal M}\\pa{#1}}
\\newcommand{\\trace}[1]{tr\\pa{#1}}
\\newcommand{\\sac}[0]{|}
\\newcommand{\\abs}[1]{\\left|#1\\right|}
"""
# \\usepackage{eepic}

imgmath_latex_preamble = preamble + custom_preamble
latex_elements['preamble'] = preamble + custom_preamble
mathdef_link_only = True

epkg_dictionary.update({
    'BaseLogging': 'http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/lightmlrestapi/mlapp/base_logging.html#lightmlrestapi.mlapp.base_logging.BaseLogging',
    'FileZilla': 'https://filezilla-project.org/',
    'format': 'https://docs.python.org/3/library/functions.html?highlight=format#format',
    'HTTP': 'https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol',
    'HTTPS': 'https://en.wikipedia.org/wiki/HTTPS',
    'HTTP 404': 'https://en.wikipedia.org/wiki/HTTP_404',
    'HTTP 500': 'https://en.wikipedia.org/wiki/List_of_HTTP_status_codes',
    'https': 'https://en.wikipedia.org/wiki/HTTPS',
    'hypercorn': 'https://pgjones.gitlab.io/hypercorn/',
    "QCM": 'https://en.wikipedia.org/wiki/Multiple_choice',
    'pyformat': 'https://github.com/myint/pyformat',
    'SessionMiddleware': 'https://github.com/encode/starlette/blob/master/starlette/middleware/sessions.py',
    'starlette': 'https://github.com/encode/starlette',
    "ujson": 'https://github.com/esnme/ultrajson',
    'uvicorn': 'https://github.com/encode/uvicorn',
    'waitress': 'https://docs.pylonsproject.org/projects/waitress/en/latest/',
    'wikipedia': 'https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal',
})
