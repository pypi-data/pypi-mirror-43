#!/usr/bin/python

from sys import argv, exit
from random import *
import numpy as np
#import importlib
from math import *

def diagonal(dimension,max_count):

    sum = ""
    sum_sqr = ""

    for i in xrange(0,dimension):

        sum += "+x[%d]" % i
        sum_sqr += "+x[%d]*x[%d]" % (i,i)


    diag_dist = "exp(((%s) - (%s)*(%s)/%d)*log(0.001)/sqrt(%d))" % (sum_sqr,sum,sum,dimension,dimension)
    func = "0.5*sin(0.5*pi + pi*((%d+1)%%2) + pi*0.5*(2*%d)*(%s)/%d)" % (max_count,max_count,sum,dimension)

    return diag_dist+"*"+func

if len(argv) < 5:
    print "Usage: %s <# of peaks> <# of dimensions> <# of samples> <output.pts>" % argv[0]
    exit()

n = int(argv[1])
d = int(argv[2])
samples = int(argv[3])

func = diagonal(d,n)
libFile = "diagonal%d_%dD.py" % (n,d)
f = open(libFile,'w')
f.write("from math import *\n")
f.write("def diagFunc(x):\n")
f.write("\tret=" + func + "\n")
f.write("\treturn ret")
f.close()

#i = importlib.import_module("diagonal%d_%dD" % (n,d))
i = __import__("diagonal%d_%dD" % (n,d))

output = open(argv[4],'w')

#Only valid for diagonal 4
nextValue = -1.
for ii in xrange(0,n+1):
  p = np.zeros(d)
  for j in xrange(0,d):
      p[j] = nextValue

  f = i.diagFunc(p)
  for pp in p:
      output.write("%f " % pp)
  output.write("%f\n" % f)
  nextValue = nextValue + 0.5

for ii in xrange(0,samples-n-1):
    p = np.random.rand(d)
    for j in xrange(0,d):
        p[j] = 2*p[j]-1

    f = i.diagFunc(p)

    for pp in p:
        output.write("%f " % pp)
    output.write("%f\n" % f)

output.close()
