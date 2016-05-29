import hilbert

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
	hilbertnums = [] 
	for coord in coords:
		hilbertNum = hilbert.Hilbert_to_int(coord)
		hilbertnums.append(hilbertNum, coord)
	hilbertnums = sorted(hilbertnums)


def minimumSpanningRectangle(coords):
	dim = len(coords[0])
	ll = list(coords[0])
	ur = list(coords[0])
	for coord in coords:
		for i in range(len(coord)):
			if coord[i] < ll[i]:
				ll[i] = coord[i]
			if coord[i] > ur[i]:
				ur[i] = coord[i]
	return (tuple(ll), tuple(ur))

coords = [(1,2,3),(2,3,4),(3,4,5),(5,6,7),(6,7,8),(7,8,9),(9,10,11),(10,11,12)]
hilbertnums = [] 
for coord in coords:
	hilbertNum = hilbert.Hilbert_to_int(coord)
	hilbertnums.append([hilbertNum, coord])

hilbertnums = sorted(hilbertnums)
# create leaf nodes
leafnodes = [] 
for leafnode in range(int(math.ceil(len(coords) / float(k)))):
	curKeys = [i[1] for i in hilbertnums[k*leafnode:k*leafnode+k]]
	node = LeafNode(curKeys)
	leafnodes.append(node)

# create higher level nodes
cur_level_nodes = leafnodes
while len(cur_level_nodes) > 1:
	next_level_nodes = [] 
	for nextLevelNode in range(int(math.ceil(len(cur_level_nodes) / float(k)))):
		curKeys = [i for i in cur_level_nodes[k*nextLevelNode:k*nextLevelNode+k]]
		node = InternalNode(curKeys)
		next_level_nodes.append(node)
	cur_level_nodes = next_level_nodes

root = cur_level_nodes[0]
printTree(root)

def height(root):
	height = 1
	temp = root
	while type(temp) == InternalNode:
		height += 1
		temp = temp.children[0]
	return height

#prints trees of height 2 or 3
def printTree(root):
	if height(root) < 3:
		print '        ' + root.toString()
		if height(root) == 2:
			print '   '.join([i.toString() for i in root.children])
	if height(root) == 3:
		print '                  ' + root.toString()
		print '      ' + '             '.join([i.toString() for i in root.children])
		print ' '.join([' '.join([i.toString() for i in j.children]) for j in root.children])



