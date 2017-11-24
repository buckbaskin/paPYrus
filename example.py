'''
Write a report describing how to convert a vector-rotation to a YXY set of
Euler Angles.

Don't forget for later:
    % \graphicspath{ {images/} }
    % \includegraphics[width=6.75in,angle=0]{Example}
'''

import helpme as h
import math
import sympy as sy

from sympy import cos, sin, latex, symbols, simplify, Matrix, MatrixSymbol

from pylatex import Document, Section, Subsection, Subsubsection, Command
from pylatex.basic import NewLine, LineBreak
from pylatex.utils import italic, NoEscape

geometry_options = {"margin": "0.69in"}
doc = Document(
    documentclass='article',
    document_options=['12pt', 'letterpaper', 'oneside', 'notitlepage', 'onecolumn'],
    fontenc=None,
    lmodern=False,
    textcomp=True,
    inputenc='utf8',
    geometry_options=geometry_options)
doc.preamble.append(Command('title', 'Vector-Rotation to Euler Angles'))
doc.preamble.append(Command('author', 'Buck Baskin'))
doc.preamble.append(Command('date', NoEscape(r'\today')))
doc.append(NoEscape(r'\maketitle'))

h.myusual(doc)

ROTATIONS = 3

def var_pattern(prefix, count):
    list_ = []
    for i in range(0, count):
        list_.append('%s%d' % (prefix, i,))
    return symbols(' '.join(list_))

def body_x(theta):
    return Matrix([[1, 0, 0],
                   [0, cos(theta), -sin(theta)],
                   [0, sin(theta), cos(theta)],
                  ])

def body_y(theta):
    return Matrix([[cos(theta), 0, sin(theta)],
                   [0, 1, 0],
                   [-sin(theta), 0, cos(theta)],
                  ])

def body_z(theta):
    return Matrix([[cos(theta), -sin(theta), 0],
                   [sin(theta), cos(theta), 0],
                   [0, 0, 1],
                  ])

a, b, g = symbols('alpha beta gamma')

h.stuff(doc, 'Some calculations were verified using Python.')

with h.section(doc, 'Answer'):
    h.stuff(doc, r'$R_{BA} = R_{y}(\alpha) R_{x}(\beta) R_{y}(\gamma)$')

    R_y_a = body_y(a)

    print('$R_{y} (\\alpha) = \n%s$\n' % (latex(R_y_a),))

    R_x_b = body_x(b)

    print('$R_{x} (\\beta) = \n%s$\n' % (latex(R_x_b),))

    R_y_g = body_y(g)

    print('$R_{y} (\\gamma) = \n%s$\n' % (latex(R_y_g),))

    print('$R_{BA} = \n%s\n%s\n%s$\n' % (latex(R_y_a), latex(R_x_b), latex(R_y_g)))

    R_AB = simplify(R_y_a * R_x_b * R_y_g)

    print('$R_{BA} = \n%s$\n' % (latex(R_AB),))

    print('% ---- %')

    w_hat = Matrix([[0, -1, 1],
                    [1, 0, -1],
                    [-1, 1, 0]]) * (1/sy.sqrt(3))

    print('$\hat{\omega} = \n%s$\n' % (latex(w_hat),))

    w_hat_2 = simplify(w_hat * w_hat)

    print('$\hat{\omega}^{2} = \n%s$\n' % (latex(w_hat_2),))

    print('$e^{\hat{\omega} \\theta} = I - \n%s\n + \n%s$\n' % (latex(w_hat), latex(w_hat_2),))

    e_hat_w_t = simplify(sy.eye(3) - w_hat + w_hat_2)

    print('$e^{\hat{\omega} \\theta} = %s = R_{BA} =$' % (latex(e_hat_w_t),))

    with h.subsection(doc, 'Solving for $\\alpha, \\beta, \\gamma$'):
        with h.subsubsection(doc, r'$\beta$'):
            h.stuff(doc,
                r'Using the atan method, one can solve for $\beta$ using the '
                'middle column of the matrix. The middle value, '
                r'$r_{22} = cos(\beta)$. Using $r_{12}^{2} + r_{32}^{2} = '
                r'sin^{2}(\beta)(sin^{2}(\gamma) + cos^{2}(\gamma)) = '
                r'sin^{2}(\beta)$, $sin(\beta) = \sqrt{r_{12}^{2} + r_{32}^{2}}$. '
                r'Therefore, $\beta = atan2(\sqrt{r_{12}^{2} + r_{32}^{2}}, r_{22})$.')
        with h.subsubsection(doc, r'$\gamma$'):
            h.stuff(doc,
                'Looking at two elements in the middle row of the matrix, one '
                'can solve for $\gamma$ using the atan method. '
                r'$r_{21} = sin(\beta) sin(\gamma)$, so $sin(\gamma) = r_{21} / '
                r'sin(\beta)$. $r_{23} = -sin(\beta) cos(\gamma)$, so '
                r'$cos(\gamma) = -r_{23} / sin(\beta)$. Therefore, '
                r'$\gamma = atan2(r_{21} / sin(\beta), -r_{23} / sin(\beta))$.')
        with h.subsubsection(doc, r'$\alpha$'):
            h.stuff(doc,
                r'$r_{12} = sin(\alpha) sin(\beta)$, $sin(\alpha) = r_{12} / '
                r'sin(\beta)$\\'
                r'$r_{32} = cos(\alpha) sin(\beta)$, $cos(\alpha) = r_{32} / '
                r'sin(\beta)$\\'
                r'$\alpha = atan2(r_{12} / sin(\beta), r_{32} / sin(\beta))$')
    with h.subsection(doc, 'Conclusion'):
        h.stuff(doc, 
            'Substituting the correct values from $R_{BA}$ calculated by '
            'Rodriguez Formula into the spaces allocated by $r_{ij}$ that were '
            'solved into an $atan2$ formula using $R_{BA}$ calculated by the '
            'rotation matrices gives the solution for the equivalent rotations '
            'in radians (rounded to 3 decimal places).')
        doc.append(NewLine())

        r12 = 1/3 + math.sqrt(3)/3
        r21 = 1/3 - math.sqrt(3)/3
        r22 = 1/3
        r23 = 1/3 + math.sqrt(3)/3
        r32 = 1/3 - math.sqrt(3)/3

        beta = math.atan2(math.sqrt(r12**2 + r32**2), r22)
        gamma = math.atan2(r21/sin(beta), -r23/sin(beta))
        alpha = math.atan2(r12/sin(beta), r32/sin(beta))

        h.stuff(doc, '$\\alpha = %.3f, \\beta = %.3f, \\gamma = %.3f$' % (alpha, beta, gamma,))

h.build(doc, 'generated')