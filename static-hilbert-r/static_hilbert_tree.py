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
	result = 0
	for i in range(len(point)):
		qi = point[i]
		ri = qi
		if qi < rect[0][i]: ri = rect[0][i]
		elif qi > rect[1][i]: ri = rect[1][i]
		result += (qi - ri)**2
	return result

# squared euclidean distance
def dist(p1, p2):
	return sum([(p1[i] - p2[i])**2 for i in range(len(p1))])

class LeafNode(object):
	def __init__(self, keyCoords, keyIds = None, ll = None, ur = None,):
		self.keyIds = keyIds
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
			q.put(child, 0)
		while not q.empty():
			element = q.get()
			if type(element) == LeafNode:
				for elem in element.keyCoords:
					q.put(elem, dist(point, elem))
			elif type(element) == InternalNode:
				for child in element.children:
					q.put(child, mindist(point, child.msr))
			else: # element is a (ll, ur)
				curdist = dist(point, element)
				curMinDist = mindist(point, q.queue[0]) if type(q.queue[0]) == InternalNode else dist(point, q.queue[0])
				# if its distance is greater than the current smallest distance in the pq
				if (not q.empty()) and (curMinDist < curdist):
					q.put(elem, curdist)
				else:
					result.append(element)
					if len(result) >= k: return result
    
	#prints trees of height 2 or 3
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
t.printTree()
