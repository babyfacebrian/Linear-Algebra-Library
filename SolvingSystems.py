from math import *
from decimal import *
from LinearSystemClass import *
from PlaneClass import *

getcontext().prec = 10


p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')

s = LinearSystem([p1,p2])

print s.compute_solution()
