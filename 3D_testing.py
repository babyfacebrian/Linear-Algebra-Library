from math import *
from decimal import *
from PlaneClass import *

getcontext().prec = 10


plane1 = Plane(normal_vector=Vector([-0.412, 3.806, 0.728]), constant_term=-3.46)
plane2 = Plane(normal_vector=Vector([1.03, -9.515, -1.82]), constant_term=8.65)

plane3 = Plane(normal_vector=Vector([2.611, 5.528, 0.283]), constant_term=4.6)
plane4 = Plane(normal_vector=Vector([7.715, 8.306, 5.342]), constant_term=3.76)

plane5 = Plane(normal_vector=Vector([-7.926, 8.625, -7.212]), constant_term=-7.952)
plane6 = Plane(normal_vector=Vector([-2.642, 2.875, -2.404]), constant_term=-2.443)


print plane1 == plane2
print plane1.is_parallel(plane2)

print plane3 == plane4
print plane3.is_parallel(plane4)

print plane5 == plane6
print plane5.is_parallel(plane6)
