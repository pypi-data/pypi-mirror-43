import random
import math
import numpy as np
import scipy
import copy



###############################################################################
# Test Functions
###############################################################################

###############################################################################
# http://math.stackexchange.com/questions/152256/implicit-equation-for-double-torus-genus-2-orientable-surface


def torusPolyGeneratorF(x, n):
    product = 1
    for i in range(1, n+1):
        product *= (x-(i-1))*(x-i)
    return product


def torusPolyGeneratorG(x, y, n):
    return (torusPolyGeneratorF(x, n) + y**2)


def doubleTorus(x, y, n=2, r=0.1, sgn=1):
    return sgn*np.sqrt(r**2 - torusPolyGeneratorG(x, y, n)**2)


# def torusPolyGeneratorF(x, y):
#     return (x**2+y**2)**2 - 4*x**2 + y**2


# def doubleTorus(x, y, r=0.1, sgn=1):
#     return sgn*np.sqrt(r**2 - torusPolyGeneratorF(x,y)**2)


def genTorusInputSampleSet(N):
    r = 0.175
    n = 2
    x = np.zeros(N)
    y = np.zeros(N)
    z = np.zeros(N)

    # Solved the roots of f(x)=r^2 using wolfram alpha and truncate to
    # make sure we don't end up with negatives under the radical.
    # Note, changing r will affect these bounds
    minX = -0.073275
    maxX = n-minX

    for i in range(N):
        ySgn = (-1)**random.randint(1, 2)
        zSgn = (-1)**random.randint(1, 2)
        # x[i] = random.uniform(0, n)
        x[i] = random.uniform(minX, maxX)

        # The distribution below requires less samples, but may be
        # harder to sell in a paper, as it is clearly non-uniform,
        # whereas the sampling in y-space makes it look more uniform due
        # to the dependence on x which yields more samples closer to
        # zero, so we bias towards the more extreme values to counteract
        # this effect.

        # x[i] = random.betavariate(0.5,0.5)*(maxX-minX) + minX

        fx = torusPolyGeneratorF(x[i], n)
        minY = np.sqrt(max(-r-fx, 0))
        maxY = np.sqrt(r-fx)
        # y[i] = ySgn*(random.uniform(minY, maxY))
        y[i] = ySgn*(random.betavariate(0.5, 0.5)*(maxY-minY) + minY)
        z[i] = doubleTorus(x[i], y[i], n, r, zSgn)
    return (x, y, z)

# End http://np.stackexchange.com/questions/152256/implicit-equation-for-double-torus-genus-2-orientable-surface
###############################################################################

def torus(u, v):
    c = 1
    a = 0.25
    x = (c+a*np.cos(v))*np.cos(u)
    y = (c+a*np.cos(v))*np.sin(u)
    z = a*np.sin(v)
    return [x, y, z]



