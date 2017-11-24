from pylatex import Document, Section, Subsection, Subsubsection, Command, UnsafeCommand
from pylatex.utils import italic, NoEscape

default_package_list = [
    'parskip',
    # \usepackage[utf8]{inputenc}
    # \usepackage[english]{babel}
    'listings',
    'color',
    'verbatim',
    'soul',
    # \usepackage[margin=0.69in]{geometry}
    'amsmath',
    'amssymb',
    'amsthm',
    'gensymb',
    'graphicx',
]

def stuff(doc, content):
    doc.append(NoEscape(content))

def myusual(doc):
    stuff(doc.preamble, NoEscape(r'\usepackage[english]{babel}'))
    stuff(doc.preamble, NoEscape(r'\usepackage[margin=0.69in]{geometry}'))

    for package in default_package_list:
        doc.preamble.append(Command('usepackage', package))

    stuff(doc.preamble, NoEscape(r'\definecolor{dkgreen}{rgb}{0, 0.6, 0}'))
    stuff(doc.preamble, NoEscape(r'\definecolor{gray}{rgb}{0.5, 0.5, 0.5}'))
    stuff(doc.preamble, NoEscape(r'\definecolor{mauve}{rgb}{0.58, 0, 0.82}'))
    stuff(doc.preamble, NoEscape(
'''\\lstset{frame=tb,
  language=Matlab,
  aboveskip=3mm,
  belowskip=3mm,
  showstringspaces=false,
  columns=flexible,
  basicstyle={\\small\\ttfamily},
  numbers=none,
  numberstyle=\\tiny\\color{gray},
  keywordstyle=\\color{blue},
  commentstyle=\\color{dkgreen},
  stringstyle=\\color{mauve},
  breaklines=true,
  breakatwhitespace=true,
  tabsize=3
}'''))

    '''
    UnsafeCommand('newcommand', '\exampleCommand', options=3,
                             extra_arguments=r'\color{#1} #2 #3 \color{black}')
    >>>
    \newcommand{\exampleCommand}[3]{\color{#1} #2 #3 \color{black}}%
    '''

    '''
        \DeclareMathOperator*{\argmax}{arg\,max}
        \DeclareMathOperator*{\argmin}{arg\,min}
    '''
    doc.preamble.append(UnsafeCommand('DeclareMathOperator*', arguments=(r'\argmax', r'arg\,max')))
    doc.preamble.append(UnsafeCommand('DeclareMathOperator*', arguments=(r'\argmin', r'arg\,min')))

    doc.preamble.append(UnsafeCommand('newcommand', '\subsubsubsection', extra_arguments=('\paragraph',)))

    doc.preamble.append(UnsafeCommand('newcommand', r'\bbs', options=1, extra_arguments=('\section{#1}',)))
    doc.preamble.append(UnsafeCommand('newcommand', r'\bbbs', options=1, extra_arguments=('\subsection{#1}',)))
    doc.preamble.append(UnsafeCommand('newcommand', r'\bbbbs', options=1, extra_arguments=('\subsubsection{#1}',)))
    doc.preamble.append(UnsafeCommand('newcommand', r'\bbbbbs', options=1, extra_arguments=('\subsubsubsection{#1}',)))
    doc.preamble.append(UnsafeCommand('newcommand', r'\norm', options=1, extra_arguments=(r'\left\lVert#1\right\rVert',)))


def build(doc, filename):
    doc.generate_pdf(filename, clean_tex=False)

def section(doc, title):
    return doc.create(Section(NoEscape(title)))

def subsection(doc, title):
    return doc.create(Subsection(NoEscape(title)))

def subsubsection(doc, title):
    return doc.create(Subsubsection(NoEscape(title)))