from sys import argv,exit
from randomDistanceField import *
from random import *
import numpy as np

if len(argv) < 4:
    print "Usage: %s <input.xml> <# of points> [<norm>] <output.pts>" % argv[0]
    exit(0)


field = randomField(argv[1])
dim = field.field.dimension

count = int(argv[2])
if len(argv) > 4:
    norm = float(argv[3])
else:
    norm = None


template = "%.12e"
for i in xrange(0,dim):
    template += " %.12e"
template += "\n"

output_str = ""

for c in field.field.centers:
    output_str += template % tuple(list(c[0]) + [0])

for i in xrange(0,count):
    p = np.random.rand(dim)
    f = field.eval(p,norm)

    output_str += template % tuple(list(p)+[f])


output = open(argv[-1],'w')
output.write(output_str)
output.close()

