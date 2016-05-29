import pickle
import numpy as np
from hilbert import gray_encode_travel, gray_decode_travel, child_start_end
from hilbert import int_to_Hilbert, Hilbert_to_int

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

(X, X_nmf, y, nmf_components, face2pics) = pickle.load(open( "nmfdata.p", "rb" ) )

def float2IntVector(vector,precision = 10.0**20):
	return [ int(elem*precision)  for elem in vector]
def int2FloatVector(vector,precision = 10.0**20):
	return [ (elem+0.0)/precision  for elem in vector]

# int_to_Hilbert( i, nD )
# def int_to_Hilbert( i, nD=2 ):  # Default is the 2D Hilbert walk.
# def Hilbert_to_int( coords ):

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


