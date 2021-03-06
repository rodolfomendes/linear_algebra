from math import sqrt, acos, pi
from decimal import Decimal,getcontext

getcontext().prec = 30

class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    TOLERANCE = 1e-10

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(str(x)) for x in coordinates])
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')
    
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __iter__(self):
        return iter(self.coordinates)

    def __getitem__(self, i):
        return self.coordinates[i]


    def __setitem__(self, i, x):
        self.coordinates[i] = x

    def plus(self, v):
        new_coordinates = [x + y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x - y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [x*Decimal(str(c)) for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return Decimal(str(sqrt(sum(coordinates_squared))))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def dot(self, v):
        dot_product = sum([x*y for x,y in zip(self.coordinates, v.coordinates)])
        return round(Decimal(dot_product), 3)

    def angle_with(self, v, in_degrees = False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = Decimal(acos(u1.dot(u2)))

            if in_degrees:
                degrees_per_radian = Decimal('180') / Decimal(pi)
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle wit the zero vector')
            else:
                raise e

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_parallel(self, v):
        return (self.is_zero() or
            v.is_zero() or
            self.angle_with(v) == 0 or
            self.angle_with(v) == pi
        )

    def is_orthogonal_to(self, v, tolerance = 1e-10):
        return abs(self.dot(v)) < tolerance

    def parallel_to(self, b):
        b_norm = b.normalized()
        return b_norm.times_scalar(self.dot(b_norm))

    def orthogonal_to(self, b):
        return self.minus(self.parallel_to(b))
