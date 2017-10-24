import numpy

#neighboring inputs change by at most 1 in exactly one list element. x is a list
def mech(eps, x):
    y = [a + numpy.random.laplace(scale=1.0/eps) for a in x]
    ind = numpy.argmax(y)
    return y[ind]
