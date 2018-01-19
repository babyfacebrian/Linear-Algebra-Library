from math import *
from decimal import *
from VectorClass import *
from LineClass import *

getcontext().prec = 10

v1 = Vector([2, 5])
v2 = Vector([2, 1])

line1 = Line(normal_vector=v1, constant_term=1)
line2 = Line(normal_vector=v2, constant_term=1)
