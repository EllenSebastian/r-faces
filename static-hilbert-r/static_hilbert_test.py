import static_hilbert_tree

coords = [(1,2,3),(2,3,4),(3,4,5),(5,6,7),(6,7,8),(7,8,9),(9,10,11),(10,11,12)]
t = static_hilbert_tree.StaticHilbertR(coords, 2)
print t.kNearestNeighbors((5,6,7),2)
print t.kNearestNeighbors((5,6,6),3)
print t.kNearestNeighbors((1,2,3),2)
print t.rangeSearch(((1,2,3),(5,6,7)))
print t.pointSearch((1,2,3))

t = static_hilbert_tree.StaticHilbertR(coords, 3)
print t.kNearestNeighbors((5,6,7),2)
print t.kNearestNeighbors((5,6,6),3)
print t.kNearestNeighbors((1,2,3),2)
print t.rangeSearch(((1,2,3),(5,6,7)))
print t.pointSearch((1,2,3))

coords = [] 
for line in open('../random_faces_50dim.csv'):
	face = [int(i) for i in line.split(',')]
	coords.append(tuple(face))

tf1 = static_hilbert_tree.StaticHilbertR(coords, 3)
tf1.printTree()
res = tf1.kNearestNeighbors(coords[0], 10) 
for i in res: print static_hilbert_tree.dist(i, coords[0])
tf1.kNearestNeighbors(tuple([1 for i in range(50)]), 4)
