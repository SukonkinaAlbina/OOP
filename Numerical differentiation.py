import math as m
import numpy as np
import sympy as smp
import matplotlib.pyplot as plt


class AbstractDerivative:
    def __init__(self, function, step):
        self.function = function
        self.step = float(step)

    def __call__(self, x):
        raise NotImplementedError


class ForwardDerivative(AbstractDerivative):
    def __init__(self, function, step, name):
        super().__init__(function, step)
        self.__name__ = name

    def __call__(self, x):
        return (self.function(x + self.step) - self.function(x)) / self.step


class BackwardDerivative(AbstractDerivative):
    def __init__(self, function, step, name):
        super().__init__(function, step)
        self.__name__ = name

    def __call__(self, x):
        return (self.function(x) - self.function(x - self.step)) / self.step


class CentralDerivative(AbstractDerivative):
    def __init__(self, function, step, name):
        super().__init__(function, step)
        self.__name__ = name

    def __call__(self, x):
        return (self.function(x + self.step) - self.function(x - self.step)) / (2 * self.step)


class FivePointsDerivative(AbstractDerivative):
    def __init__(self, function, step, name):
        super().__init__(function, step)
        self.__name__ = name

    def __call__(self, x):
        return 4 / (2 * 3 * self.step) * (self.function(x + self.step) - self.function(x - self.step)) - \
               (1 / (3 * 4 * self.step)) * (self.function(x + 2 * self.step) - self.function(x - 2 * self.step))


class SevenPointsDerivative(AbstractDerivative):
    def __init__(self, function, step, name):
        super().__init__(function, step)
        self.__name__ = name

    def __call__(self, x):
        return (3 / (4 * self.step)) * (self.function(x + self.step) - self.function(x - self.step)) - \
               (3 / (4 * 5 * self.step)) * (self.function(x + 2 * self.step) - self.function(x - 2 * self.step)) + \
               (1 / (10 * 6 * self.step)) * (self.function(x + 3 * self.step) - self.function(x - 3 * self.step))


def derivatives_plot():
    function, analiticalDerivative = listOfFunctions[i], listOfAnaliticalDerivatives[i]
    errors = {}
    print('Function %s\n' % (listOfSymbolicFunctions[i]))
    for h in listOfSteps:
        list_of_formula = [ForwardDerivative(function, h, 'ForwardDerivative'),
                           BackwardDerivative(function, h, 'BackwardDerivative'),
                           CentralDerivative(function, h, 'CentralDerivative'),
                           FivePointsDerivative(function, h, 'FivePointsDerivative'),
                           SevenPointsDerivative(function, h, 'SevenPointsDerivative')]
        for formula in list_of_formula:
            errors.setdefault(formula.__name__, [])
            error = m.fabs(formula(x0) - analiticalDerivative(x0))
            errors[formula.__name__].append(error)
    plt.figure(figsize=figureSizeConst)
    plt.title('Convergence', fontsize=15)
    for formula_name in errors:
        plt.loglog(np.array(listOfSteps), np.array(errors[formula_name]), 'v-', markersize=10, linewidth=2,
                   label=formula_name)
    plt.legend(loc="best")
    plt.grid('on')
    plt.ylim([1e-17, 10.])
    plt.xlabel('h')
    plt.ylabel('Global error')
    plt.show()


xSym = smp.Symbol('x')
# Функции в символьном представлении
listOfSymbolicFunctions = [smp.sin(xSym ** 2), smp.cos(smp.sin(xSym)), smp.exp(smp.sin(smp.cos(xSym))),
                           smp.log(xSym + 3.), smp.sqrt(xSym + 3.)]
# Представление символьных функций в виде функций Python
listOfFunctions = [smp.lambdify(xSym, f) for f in listOfSymbolicFunctions]
# Производные в символьном представлении
listOfSymbolicDerivatives = [smp.diff(f, xSym) for f in listOfSymbolicFunctions]
# Представление символьных производных в виде функций Python
listOfAnaliticalDerivatives = [smp.lambdify(xSym, f) for f in listOfSymbolicDerivatives]

xLeft, xRight = 0., 100.
numPoints = 100
figureSizeConst = (13, 6.7)
x0 = .5
listOfSteps = [2 ** (1 - n) for n in range(1, 21)]

for i in range(len(listOfSymbolicFunctions)):
    derivatives_plot()
