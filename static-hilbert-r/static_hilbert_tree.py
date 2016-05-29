import hilbert
import math 
import Queue

def minimumSpanningRectangle(coords):
	ll = list(coords[0])
	ur = list(coords[0])
	for coord in coords:
		for i in range(len(coord)):
			if coord[i] < ll[i]:
				ll[i] = coord[i]
			if coord[i] > ur[i]:
				ur[i] = coord[i]
	return (tuple(ll), tuple(ur))

def rectContainsPoint(rect, point):
	for i in range(len(point)):
		if rect[0][i] > point[i] or rect[1][i] < point[i]:
			return False
	return True

def rectsIntersect(rect1, rect2):
	for i in range(len(rect1[0])):
		if rect1[0][i] > rect2[1][i]: return False
		if rect2[0][i] > rect1[1][i]: return False 
	return True

# minmum distance btween a point an a rectangle as in 4.3.1 on p56
def mindist(point, rect):
	# if rect contains point, then its 0.
	if rectContainsPoint(rect, point): return 0
	result = 0
	for i in range(len(point)):
		qi = point[i]
		si = rect[0][i]
		ti = rect[0][i]
		ri = qi
		if qi < si: ri = si
		if qi > ti: ri = ti
		result += (qi - ri)**2
	return result

# squared euclidean distance
def dist(p1, p2):
	return sum([(p1[i] - p2[i])**2 for i in range(len(p1))])

class LeafNode(object):
	def __init__(self, keyCoords, keyAux = None, ll = None, ur = None,):
		self.keyAux = keyAux
		self.keyCoords = keyCoords
		if ll is None or ur is None:
			self.msr = minimumSpanningRectangle(keyCoords)
		else:
			self.msr = (ll, ur)
	def toString(self):
		return '(' + ','.join([str(i) for i in self.msr[0]]) + ')-(' + ','.join([str(i) for i in self.msr[1]]) + ')'
	def searchPoint(self, point):
		return [i for i in self.keyCoords if point == i]
	def searchRect(self, rect):
		return [i for i in self.keyCoords if rectContainsPoint(rect, i)]


class InternalNode(object):
	def __init__(self, children):
		self.children = children
		allcoords = []
		for child in children:
			allcoords.append(child.msr[0])
			allcoords.append(child.msr[1])
		self.msr = minimumSpanningRectangle(allcoords)
	def toString(self):
		return '(' + ','.join([str(i) for i in self.msr[0]]) + ')-(' + ','.join([str(i) for i in self.msr[1]]) + ')'

class StaticHilbertR(object):
	def __init__(self, coords, k):
		hilbertnums = sorted([[hilbert.Hilbert_to_int(coord), coord] for coord in coords])
		# create leaf nodes
		leafnodes = [] 
		for leafnode in range(int(math.ceil(len(coords) / float(k)))):
			curKeys = [i[1] for i in hilbertnums[k*leafnode:k*leafnode+k]]
			node = LeafNode(curKeys)
			leafnodes.append(node)
		self.height = 1
		# create higher level nodes
		curLevelNodes = leafnodes
		while len(curLevelNodes) > 1:
			self.height += 1
			nextLevelNodes = [] 
			for nextLevelNode in range(int(math.ceil(len(curLevelNodes) / float(k)))):
				curKeys = [i for i in curLevelNodes[k*nextLevelNode:k*nextLevelNode+k]]
				node = InternalNode(curKeys)
				nextLevelNodes.append(node)
			curLevelNodes = nextLevelNodes
		self.root = curLevelNodes[0]
    
	def pointSearchRec(self, point, curNode):
		if type(curNode) == LeafNode: # case where root is a leaf is already covered pointSearch
			return curNode.searchPoint(point)
		else:
			result = [] 
			for child in curNode.children:
				if rectContainsPoint(child.msr, point):
					result += self.pointSearchRec(point, child)
		return result
    
	def rangeSearchRec(self, rect, curNode):
		if type(curNode) == LeafNode:
			return curNode.searchRect(rect)
		else:
			result = [] 
			for child in curNode.children:
				if rectsIntersect(child.msr, rect):
					result += self.rangeSearchRec(rect, child)
		return result
    
	# return all entries that intersect with rect.
	def rangeSearch(self, rect):
		if rectsIntersect(self.root.msr, rect):		
			return self.rangeSearchRec(rect, self.root)
    
	def pointSearch(self, point):
		if rectContainsPoint(self.root.msr, point):
			return self.pointSearchRec(point, self.root)
		return []
        
	# incremental nearest neighbor search as in R tree book, p.60.
	def kNearestNeighbors(self, point, k):
		result = [] 
		q = Queue.PriorityQueue() # put(item, priority), lower priority is dequeued first
		for child in self.root.children:
			print 'enqueue roots child mindist: ', mindist(point,child.msr)
			q.put((mindist(point, child.msr), child)) # or priority 0?
		while not q.empty():
			element = q.get()[1]
			if type(element) == LeafNode:
				print 'dequeued leafnode ', element.msr[0][0], 'with dist ', mindist(point, element.msr)
				for elem in element.keyCoords:
					print 'enqueue leafnode key',elem[0],' dist: ', dist(point, elem)
					q.put((dist(point, elem), elem))
			elif type(element) == InternalNode:
				print 'dequeued internalnode', element.msr[0][0], 'with dist ', mindist(point, element.msr)
				for child in element.children:
					print 'enqueue internalnode child',child.msr[0][0],' dist: ', mindist(point, child.msr)
					q.put((mindist(point, child.msr), child))
			else: # element is a (ll, ur)
				print 'dequeued obj', element[0], 'with dist ', dist(point, element)
				curdist = dist(point, element)
				curMinDist = 0
				print 'top of queue:', q.queue[0]
				print type(q.queue[0][1])
				if type(q.queue[0][1]) == InternalNode:
					print 'use mindist'
					curMinDist = mindist(point, q.queue[0][1].msr)
				elif type(q.queue[0][1]) == LeafNode:
					curMinDist = mindist(point, q.queue[0][1].msr)
					print 'dist: ', curMinDist
				else:
					curMinDist = dist(point, q.queue[0][1])
				# if its distance is greater than the current smallest distance in the pq
				if (not q.empty()) and (curMinDist < curdist):
					q.put((curdist, elem))
				else:
					result.append(element)
					if len(result) >= k: return result
    

tf1 = StaticHilbertR(coords[:100],3)
tf1.kNearestNeighbors(coords[0], 3) # issue: does NOT give back coords[0] as a nearest neigbor of itself

	#prints trees of height 2 or 3 best
	def printTree(self):
		if self.height < 3:
			print '        ' + self.root.toString()
			if self.height == 2:
				print '   '.join([i.toString() for i in self.root.children])
		if self.height >= 3:
			print '                  ' + self.root.toString()
			print '      ' + '             '.join([i.toString() for i in self.root.children])
			print ' '.join([' '.join([i.toString() for i in j.children]) for j in self.root.children])


coords = [(1,2,3),(2,3,4),(3,4,5),(5,6,7),(6,7,8),(7,8,9),(9,10,11),(10,11,12)]
t = StaticHilbertR(coords, 2)
print t.kNearestNeighbors((5,6,7),2)
print t.kNearestNeighbors((5,6,6),3)
print t.kNearestNeighbors((1,2,3),2)
print t.rangeSearch(((1,2,3),(5,6,7)))
print t.pointSearch((1,2,3))

t = StaticHilbertR(coords, 3)
print t.kNearestNeighbors((5,6,7),2)
print t.kNearestNeighbors((5,6,6),3)
print t.kNearestNeighbors((1,2,3),2)
print t.rangeSearch(((1,2,3),(5,6,7)))
print t.pointSearch((1,2,3))

coords = [] 
for line in open('../random_faces_50dim.csv'):
	face = [int(i) for i in line.split(',')]
	coords.append(tuple(face))

tf = StaticHilbertR(coords, 3)
tf.printTree()
tf1 = StaticHilbertR(coords[:100],3)
tf1.kNearestNeighbors(coords[0], 3) # issue: does NOT give back coords[0] as a nearest neigbor of itself
# probably is a bug in mindist
# pointsearch does give back coords[0]

tf.kNearestNeighbors(tuple([1 for i in range(50)]), 4)
t.printTree()
