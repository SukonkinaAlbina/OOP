import sympy as smp


class AbstractIntegral:
    def __init__(self, function, left_bound, right_bound, points_count):
        self.function = function
        self.left_bound = float(left_bound)
        self.right_bound = float(right_bound)
        self.points_count = points_count
        self.coeffs = [0] * (points_count + 1)
        self.h = (self.right_bound - self.left_bound) / self.points_count
        self.x_grid = [self.left_bound + i * self.h for i in range(self.points_count + 1)]

    def __call__(self):
        res = 0
        for c, x in zip(self.coeffs, self.x_grid):
            res += c * self.function(x)
        return self.h * res


class LeftRectangle(AbstractIntegral):
    def __init__(self, *args):
        super().__init__(*args)
        self.coeffs = [1 if i != self.points_count else 0 for i in range(self.points_count + 1)]


class RightRectangle(AbstractIntegral):
    def __init__(self, *args):
        super().__init__(*args)
        self.coeffs = [1 if i != 0 else 0 for i in range(self.points_count + 1)]


class MiddleRectangle(AbstractIntegral):
    def __init__(self, *args):
        super().__init__(*args)
        self.coeffs = [1 for i in range(self.points_count + 1)]
        self.x_grid = [(self.left_bound + self.h / 2) + i * self.h for i in range(self.points_count)]


class Trapezium(AbstractIntegral):
    def __init__(self, *args):
        super().__init__(*args)
        self.coeffs = [0.5 if (i == 0 or i == self.points_count) else 1 for i in range(self.points_count + 1)]


class Sympson(AbstractIntegral):
    def __init__(self, *args):
        super().__init__(*args)
        self.check_points_count()
        for i in range(self.points_count + 1):
            if i == 0 or i == self.points_count:
                self.coeffs[i] = 1 / 3
            elif i % 2 == 0:
                self.coeffs[i] = 2 / 3
            else:
                self.coeffs[i] = 4 / 3

    def check_points_count(self):
        if self.points_count % 2 != 0:
            raise Exception('Число разбиений отрезка должно быть чётным!')


xSym = smp.Symbol('x')
# Функции в символьном представлении
SymbolicFunction = smp.cos(xSym)
# Представление символьных функций в виде функций Python
Function = smp.lambdify(xSym, SymbolicFunction)

g = MiddleRectangle(Function, 0, 1, 10)
print(g())
