import pickle
import numpy as np
from hilbert import gray_encode_travel, gray_decode_travel, child_start_end
from hilbert import int_to_Hilbert, Hilbert_to_int
from sklearn.datasets import fetch_lfw_people
import matplotlib.pyplot as plt

# Minimum bounding rectangle
def MBR(datapoints):
	n_points, m_features = datapoints.shape
	tuples = []
	for i in range(m_features):
		currmin, currmax= float("inf"),float("-inf")
		for v in datapoints:
			if v[i]>currmax:
				currmax=v[i]
			if v[i]<currmin:
				currmin=v[i]
		tuples.append((currmin,currmax))
	return tuples

def MBR2Centroid(datatuples):
	return [int((tup[1]-tup[0])/2)  for tup in datatuples]

def float2IntVector(vector,precision = 10.0**20):
	return [ int(elem*precision)  for elem in vector]
def int2FloatVector(vector,precision = 10.0**20):
	return [ (elem+0.0)/precision  for elem in vector]



def recompose_from_eigenfaces(X_pca,eigenfaces):
	if X_pca.ndim == 1:
		return sum([  X_pca[j]*eigenfaces[j] for j in range(len(X_pca)) ])
	else:
		n_examples, n_components = X_pca.shape
		X_recomposed = []
		for i in range(n_examples):
			X_recomposed.append(sum([  X_pca[i,j]*eigenfaces[j] for j in range(n_components) ]))
		return X_recomposed

# A mapping from person to pictures that represent them
# Returns [n_examples X ['name',[vector of pictures indices]]}

# If needed...
def generateface2picsmapping(minimum_faces_per_person=1):
	lfw_people = fetch_lfw_people(min_faces_per_person=minimum_faces_per_person, resize=0.4)
	n_samples, h, w = lfw_people.images.shape
	X, y, target_names = lfw_people.data, lfw_people.target, lfw_people.target_names
	n_examples, n_features = X.shape
	face2pics = []
	print(max(y))
	for i in range((max(y)+1)):
		face2pics.append([target_names[i],[] ])
	for i in range(len(y)):
		face2pics[y[i]][1].append(i)
	return face2pics

if __name__ == "__main__":
	(X, X_nmf, y, nmf_components, min_faces_per_person, face2pics) = pickle.load(open( "nmfdata.p", "rb" ) )

	n_examples, n_features = X_nmf.shape
	print(X_nmf[0])
	i = Hilbert_to_int( float2IntVector(X_nmf[0] ))
	print(i)
	v2 = int2FloatVector(int_to_Hilbert( i, nD=n_features ))
	print(v2)
	i2 = Hilbert_to_int( float2IntVector(v2 ))
	print(i2)
	print('loss')
	print(i2-i)



