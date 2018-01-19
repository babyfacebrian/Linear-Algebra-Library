from math import *
from decimal import *
from PlaneClass import *
from VectorClass import *
from copy import deepcopy

getcontext().prec = 10

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]



    def multiply_coefficient_and_row(self, coefficient, row):
        new_normal_vector = self[row].normal_vector.multiply_scalar(coefficient)
        new_constant = self[row].constant_term * coefficient
        self[row] = Plane(normal_vector=new_normal_vector, constant_term=new_constant)


    def add_multiple_times_row_to_row(self, coefficient, add_row, return_row):
        n1 = self[add_row].normal_vector
        n2 = self[return_row].normal_vector
        k1 = self[add_row].constant_term
        k2 = self[return_row].constant_term

        new_normal_vector = n1.multiply_scalar(coefficient).__add__(n2)
        new_constant = (k1 * coefficient) + k2

        self[return_row] = Plane(normal_vector=new_normal_vector, constant_term=new_constant)


    def swap_row_below(self, row, col):
        num_equations = len(self)
        for k in range(row+1, num_equations):
            coefficient = MyDecimal(self[k].normal_vector.coordinates[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True

        return False


    def clear_coefficients(self, row, col):
        num_equations = len(self)
        beta = MyDecimal(self[row].normal_vector.coordinates[col])

        for k in range(row+1, num_equations):
            gamma = self[k].normal_vector.coordinates[col]
            alpha = -gamma/beta
            self.add_multiple_times_row_to_row(alpha,row,col)



    def triangular_form(self):
        tri_system = deepcopy(self)
        num_equations = len(tri_system)
        num_variables = tri_system.dimension
        count = 0

        for i in range(num_equations):
            while count < num_variables:
                index = MyDecimal(tri_system[i].normal_vector.coordinates[count])
                if index.is_near_zero():
                    swap_suceeded = tri_system.swap_row_below(i, count)
                    if not swap_suceeded:
                        count += 1
                        continue
                tri_system.clear_coefficients(i, count)
                count += 1
                break

        return tri_system



    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension
        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret
