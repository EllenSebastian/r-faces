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
import matplotlib.patches as mpatches


def float2IntVector(vector,precision = 10.0**20):
    return [ int(elem*precision)  for elem in vector]


(X, X_nmf, y, nmf_components, face2pics) = pickle.load(open( "./alex/nmfdata.p", "rb" ) )



def createIndex(coords, k=10):
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

def getRTree(coords, k=10):
    t = createIndex(coords, k)
    t.rangeSearch = t.intersection
    return t

def getRTree2():
    dim = len(faces[0][1])
    p = index.Property()
    p.dimension = dim
    t = index.Index(properties = p)
    t.rangeSearch = t.intersection
    return t

faces = [float2IntVector(X_nmf[i]) for i in range(2000)]

############################ rangesearch line plots
x_vals = [10, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
standard_range = [0] * len(x_vals) 
hilbert_range = [0] * len(x_vals)
for n_i in range(len(x_vals)):
    n = x_vals[n_i]
    curfaces = faces[:n]
    static = getStaticHilbertTree(curfaces, 100)
    regular = getRTree(curfaces, 10)
    for i in range(0, 50):
        rand_int = random.randint(0, len(curfaces)-1)
        rand_int2 = random.randint(0, len(curfaces)-1)
        randFace = list(curfaces[max(rand_int2, rand_int)])
        randFace2 = list(curfaces[max(rand_int2, rand_int)])
        t1 = (tuple(randFace), tuple(randFace2))
        t3 = tuple(randFace + randFace2)
        time1 = time.clock()
        r = static.rangeSearch(t1)
        time2 = time.clock()
        r = regular.intersection(t3)
        time3 = time.clock()
        standard_range[n_i] += (time3 - time2) / 50.0
        hilbert_range[n_i] += (time2 - time1) / 50.0
    print standard_range, hilbert_range


f, ax = plt.subplots()
ax.set_ylabel('Time (Microseconds, CPU Time) - average over 20 random queries')
ax.set_xlabel('Number of Entries')
title = 'RangeSearch Time vs Size'
ax.set_title(title)

# red dashes, blue squares
ax.plot(x_vals, hilbert_range, 'rs--')
ax.plot(x_vals, standard_range, 'bs--')

red_patch = mpatches.Patch(color='red', label='Static Hilbert Tree RangeSearch')
blue_patch = mpatches.Patch(color='blue', label='Standard R Tree RangeSearch')
ax.legend(handles=[red_patch, blue_patch], loc=4)

plt.show()

############ pointsearch

standard_point = [0] * len(x_vals) 
hilbert_point = [0] * len(x_vals)
for n_i in range(len(x_vals)):
    n = x_vals[n_i]
    curfaces = faces[:n]
    static = getStaticHilbertTree(curfaces, 2)
    regular = getRTree(curfaces, 100)
    for i in range(0, 10):
        rand_int = random.randint(0, len(curfaces)-1)
        randFace = list(curfaces[rand_int])
        t1 = tuple(randFace)
        t2 = tuple(randFace + randFace)
        time1 = time.clock()
        r = static.pointSearch(t1)
        time2 = time.clock()
        r = regular.intersection(t2)
        time3 = time.clock()
        standard_point[n_i] += (time3 - time2) / 10.0
        hilbert_point[n_i] += (time2 - time1) / 10.0
    print standard_point, hilbert_point


f, ax = plt.subplots()
ax.set_ylabel('Time (Microseconds, CPU Time) - average over 10 random queries')
ax.set_xlabel('Number of Entries')
title = 'PointSearch Time vs Size'
ax.set_title(title)

# red dashes, blue squares
ax.plot(x_vals, hilbert_point, 'rs--')
ax.plot(x_vals, standard_point, 'bs--')

red_patch = mpatches.Patch(color='red', label='Static Hilbert Tree PointSearch')
blue_patch = mpatches.Patch(color='blue', label='Standard R Tree PointSearch')
ax.legend(handles=[red_patch, blue_patch], loc=2)

plt.show()


############ knn

standard_knn = [0] * len(x_vals) 
hilbert_knn = [0] * len(x_vals)
for n_i in range(len(x_vals)):
    n = x_vals[n_i]
    curfaces = faces[:n]
    static = getStaticHilbertTree(curfaces, 2)
    regular = getRTree(curfaces, 100)
    for i in range(0, 10):
        rand_int = random.randint(0, len(curfaces)-1)
        randFace = list(curfaces[rand_int])
        t1 = tuple(randFace)
        t2 = tuple(randFace + randFace)
        time1 = time.clock()
        r = static.kNearestNeighbors(t1, 10)
        time2 = time.clock()
        r = regular.nearest(t2, 10)
        time3 = time.clock()
        standard_knn[n_i] += (time3 - time2) / 10.0
        hilbert_knn[n_i] += (time2 - time1) / 10.0
    print standard_knn, hilbert_knn



f, ax = plt.subplots()
ax.set_ylabel('Time (Microseconds, CPU Time) - average over 10 random queries')
ax.set_xlabel('Number of Entries')
title = 'kNN Time vs Size'
ax.set_title(title)

# red dashes, blue squares
ax.plot(x_vals, hilbert_knn, 'rs--')
ax.plot(x_vals, standard_knn, 'bs--')

red_patch = mpatches.Patch(color='red', label='Static Hilbert Tree kNN')
blue_patch = mpatches.Patch(color='blue', label='Standard R Tree kNN')
ax.legend(handles=[red_patch, blue_patch], loc=2)

plt.show()

