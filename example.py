'''
Write a report describing how to convert a vector-rotation to a YXY set of
Euler Angles.

Don't forget for later:
    % \graphicspath{ {images/} }
    % \includegraphics[width=6.75in,angle=0]{Example}
'''

import math
import sympy as sy

from helpme import stuff, build, myusual
from sympy import cos, sin, latex, symbols, simplify, Matrix, MatrixSymbol

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

doc = Document('plain')
doc.preamble.append(Command('title', 'Vector-Rotation to Euler Angles'))
doc.preamble.append(Command('author', 'Buck Baskin'))
doc.preamble.append(Command('date', NoEscape(r'\today')))
doc.append(NoEscape(r'\maketitle'))

myusual(doc)

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

stuff(doc, NoEscape('$R_{BA} = R_{y}(\\alpha) R_{x}(\\beta) R_{y}(\\gamma)$\n'))

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


print('%% ---- %%')

r12 = 1/3 + math.sqrt(3)/3
r21 = 1/3 - math.sqrt(3)/3
r22 = 1/3
r23 = 1/3 + math.sqrt(3)/3
r32 = 1/3 - math.sqrt(3)/3

beta = math.atan2(math.sqrt(r12**2 + r32**2), r22)
gamma = math.atan2(r21/sin(beta), -r23/sin(beta))
alpha = math.atan2(r12/sin(beta), r32/sin(beta))

print('$\\alpha = %.3f, \\beta = %.3f, \\gamma = %.3f$' % (alpha, beta, gamma,))

build(doc, 'generated')