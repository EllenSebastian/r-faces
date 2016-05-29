#import sys
#sys.path.insert(0,'hilbertr/python')
#import rtree as hilbertr
#import rtree.rtree as hilbertrtree



# 4 dimensional r tree example
from rtree import index
p = index.Property()
p.dimension = 4
# if this gives a "InvalidPageException: unknown page id 1", try quit()ing python and starting again.
idx4d = index.Index('4d_index',properties=p)
ll = (0, 0, 60, 80) # coordinates of lower-left point of box
ur = (70, 23, 82, 106) # coordinates of upper-right point of box
# if you get a "wrong number of dimensions" error, try giving the index a different name. 
idx4d.insert(0, (ll[0], ll[1], ll[2], ll[3], ur[0], ur[1], ur[2], ur[3]))
# use intersection to find a generator of elements that intersect the given box
list(idx4d.intersection( (-1, -1, 59, 79, 71, 25, 74, 108)))



# creating rtree index for a csv file where each row is a face (sample)
# and each column is a dimension
import random

faces_file = 'random_faces_50dim.csv'
from time import strftime

f = open(faces_file,'w')
for face in range(0,1000):
	pcas = [random.randrange(0,1000) for i in range(0,50)]
	f.write(','.join([str(i) for i in pcas]) + '\n')

f.close()

faces = [[int(i) for i in line.split(',')] for line in open(faces_file)]
dim = len(faces[0])
p = index.Property()
p.dimension = dim
faceIdx = index.Index('face_index' + strftime('%m%d_%H:%M:%S'), properties = p)
faceid = 0
for face in faces:
	rectangle = tuple(face + face)
	faceIdx.insert(faceid, rectangle)
	faceid += 1
	print faceid

# find faces intersecting wiht the last face (which is just the last face)
list(faceIdx.intersection(face))

# find k closest faces to the last one
k = 5
list(faceIdx.nearest(face, 5))