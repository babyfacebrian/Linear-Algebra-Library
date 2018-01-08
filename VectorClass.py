from math import *
from decimal import *

getcontext().prec = 10

class Vector(object):

    CANNOT_NORMALISE_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'Vectors do not have a parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'Vectors do not have a orthogonal component'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimenstion = len(coordinates)
        except ValueError:
            raise ValueError('The coordinates must not be empty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, compare_vector):
        return self.coordinates == compare_vector.coordinates


    def __add__(self, v2):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v2.coordinates)]
        return Vector(new_coordinates)


    def __sub__(self, v2):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v2.coordinates)]
        return Vector(new_coordinates)


    def multiply_scalar(self, scalar):
        new_coordinates = [Decimal(scalar) * x for x in self.coordinates]
        return Vector(new_coordinates)


    def magnitude(self):
        return Decimal(sqrt(sum(x**2 for x in self.coordinates)))


    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.multiply_scalar(Decimal(1.0)/magnitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALISE_VECTOR_MSG)


    def dot_product(self, v2):
        return sum([(x*y) for x,y in zip(self.coordinates, v2.coordinates)])


    def angle(self, v2, in_degrees=False):
          try:
              u1 = self.normalized()
              u2 = v2.normalized()
              angle_in_rad = Decimal(acos(u1.dot_product(u2)))

              if in_degrees:
                  deg_per_rad = Decimal(180/pi)
                  return angle_in_rad * deg_per_rad
              else:
                  return angle_in_rad
          except Exception as e:
              if str(e) == self.CANNOT_NORMALISE_VECTOR_MSG:
                  raise Exception('Cannot compute an angle with the zero vector')
              else:
                  raise e


    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance


    def is_orthogonal(self, v2, tolerance=1e-10):
        return abs(self.dot_product(v2)) == 0


    def is_parallel(self,v2):
        # percision errors due to rounding
        angle_rounded = round(self.angle(v2,True) ,2)

        return (self.is_zero() or v2.is_zero() or
                angle_rounded == round(180, 2) or angle_rounded == 0)


    def projected_vector(self, basis):
        try:
            return basis.normalized().multiply_scalar(self.dot_product(basis.normalized()))
        except Exception as e:
            if str(e) == self.CANNOT_NORMALISE_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e


    def perpendicular(self,basis):
        try:
            return self.__sub__(self.projected_vector(basis))
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e


    def cross_product(self, v2):
        new_x = (self.coordinates[1] * v2.coordinates[2]) - (v2.coordinates[1] * self.coordinates[2])
        new_y =  Decimal(-1) * ((self.coordinates[0] * v2.coordinates[2]) - (v2.coordinates[0] * self.coordinates[2]))
        new_z = (self.coordinates[0] * v2.coordinates[1]) - (v2.coordinates[0] * self.coordinates[1])
        return Vector([new_x, new_y, new_z])


    def area_of_parallelogram(self, v2):
        para = Decimal(self.cross_product(v2).magnitude())
        return 'Area of parallelogram: {}'.format(round(para, 3))


    def area_of_triangle(self, v2):
        tri = Decimal(0.5) * self.cross_product(v2).magnitude()
        return 'Area of triangle: {}'.format(round(tri, 3))
