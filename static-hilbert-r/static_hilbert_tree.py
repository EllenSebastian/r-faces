import hilbert
import math 


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

class LeafNode(object):
	def __init__(self, keyCoords, keyIds = None, ll = None, ur = None,):
		self.keyIds = keyIds
		self.keyCoords = keyCoords
		if ll is None or ur is None:
			self.ll, self.ur = minimumSpanningRectangle(keyCoords)
		else:
			self.ll = ll
			self.ur = ur
	def toString(self):
		return '(' + ','.join([str(i) for i in self.ll]) + ')-(' + ','.join([str(i) for i in self.ur]) + ')'


class InternalNode(object):
	def __init__(self, children):
		self.children = children
		allcoords = []
		for child in children:
			allcoords.append(child.ll)
			allcoords.append(child.ur)
		self.ll, self.ur = minimumSpanningRectangle(allcoords)
	def toString(self):
		return '(' + ','.join([str(i) for i in self.ll]) + ')-(' + ','.join([str(i) for i in self.ur]) + ')'

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
                
	#prints trees of height 2 or 3
	def printTree(self):
		if self.height < 3:
			print '        ' + self.root.toString()
			if self.height == 2:
				print '   '.join([i.toString() for i in self.root.children])
		if self.height == 3:
			print '                  ' + self.root.toString()
			print '      ' + '             '.join([i.toString() for i in self.root.children])
			print ' '.join([' '.join([i.toString() for i in j.children]) for j in self.root.children])


coords = [(1,2,3),(2,3,4),(3,4,5),(5,6,7),(6,7,8),(7,8,9),(9,10,11),(10,11,12)]
t = StaticHilbertR(coords, 2)
t.printTree()
