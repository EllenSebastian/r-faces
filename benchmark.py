# creating rtree index for a csv file where each row is a face (sample)
# and each column is a dimension
import random
import time
from rtree import index
from time import strftime
import sys
sys.path.insert(0, './static-hilbert-r')
import static_hilbert_tree
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import pickle
sys.path.insert(0, './alex')
from functionsTest import float2IntVector as float2IntVector
import matplotlib.patches as mpatches

(X, X_nmf, y, nmf_components, min_faces_per_person, face2pics) = pickle.load(open( "./alex/nmfdata.p", "rb" ) )

faces_file = 'random_faces_50dim.csv'
def createFile():
    f = open(faces_file,'w')
    for face in range(0,1000):
        pcas = [random.randrange(0,1000) for i in range(0,50)]
        f.write(','.join([str(i) for i in pcas]) + '\n')

    f.close()


def createIndex(coords):
    dim = len(faces[0])
    p = index.Property()
    p.dimension = dim
    faceIdx = index.Index(properties = p)
    faceid = 0
    for face in faces:
        rectangle = tuple(face + face)
        faceIdx.insert(faceid, rectangle, face)
        faceid += 1
    return faceIdx

def getStaticHilbertTree(coords, k):
    t = static_hilbert_tree.StaticHilbertR(coords, k)
    t.nearest = t.kNearestNeighbors
    t.intersection = t.pointSearch
    return t

def getRTree(coords):
    t = createIndex(coords)
    t.rangeSearch = t.intersection
    return t

#faces = [[int(i) for i in line.split(',')] for line in open(faces_file)]
#faces = pickle.load(open( "./faces.p", "rb" ) )
total = 2000
interval = 200
faces = [float2IntVector(i) for i in X_nmf[:total]]

# TREE CREATION
x_vals = [i for i in range(0,total+interval, interval)]
data1 = []
data2 = []
#for i in x_vals:
#    time1 = time.clock()
#    getStaticHilbertTree(faces[:i], 2)
#    time2 = time.clock()
#    print '%s function took %0.3f ticks' % ("Intersection", (time2-time1))
#    data1.append((time2-time1))

for i in x_vals:
    time1 = time.time()
    getRTree(faces[:i])
    time2 = time.time()
    print '%s function took %0.3f ticks' % ("Intersection", (time2-time1))
    data2.append((time2-time1))

f, ax = plt.subplots()
ax.set_ylabel('Time (Microseconds, CPU Time)')
ax.set_xlabel('Number of Entries')
title = 'Tree Creation Time vs Size (R Tree)'
ax.set_title(title)

# red dashes, blue squares
#ax.plot(x_vals, data1, 'rs--', x_vals, data2, 'bs--')
ax.plot(x_vals, data2, 'bs--')
red_patch = mpatches.Patch(color='red', label='Static Hilbert Tree')
blue_patch = mpatches.Patch(color='blue', label='R Tree')
ax.legend(handles=[red_patch, blue_patch])

pylab.savefig(title+'.png')
plt.show()
sys.exit()


trees = {"static":getStaticHilbertTree(faces, 2), "regular":getRTree(faces)}
#trees = {"static":getStaticHilbertTree(faces, 2)}
# There doesnt seem to be a rangeSearch for regular R-Trees http://toblerity.org/rtree/class.html
functions = ["nearest", "intersection", "rangeSearch"]
k = 5
n = 10
args = {"nearest_list":[k], "regular_nearest_dict":{"objects":"raw"}, "intersection_nearest_dict":{"objects":"raw"}} 

data = [] 
f, ax = plt.subplots()
for tree_type, tree in trees.iteritems():
    print tree_type
    function = "rangeSearch"
    l_key = function + "_list"
    d_key = tree_type + "_" + function + "_dict"  
    l = []
    d = {}
    if l_key in args:
        l = args[l_key]
    if d_key in args:
        d = args[d_key]
    func = getattr(tree, function)
     
    
    times = []
    for i in range(0, n):
        rand_int = random.randint(0, len(faces)-1)
        randFace = list(faces[rand_int])

        rand_int2 = random.randint(0, len(faces)-1)
        randFace2 = list(faces[rand_int])

        old_length = len (randFace)
        time1 = time.clock()
        if tree_type == "regular":
            new_l = [randFace, randFace2] + l
        else:
            new_l = [[randFace]+ [randFace2]] + l
        #new_l = [randFace] + l
        func(*new_l, **d)
        time2 = time.clock()
        print '%s function took %0.3f ticks' % (function, (time2-time1))
        times.append((time2-time1))
        new_length = len(randFace)
    data.append(times)

labels = ["Static Hilbert Tree", "R Tree"] 
#labels = ["Static Hilbert Tree"] 
ax.boxplot(data, labels=labels)
ax.set_ylabel('Time (Microseconds, CPU Time)')
title = 'Range Search (N=2000)'
ax.set_title(title)

pylab.savefig(title+'.png')
plt.show()