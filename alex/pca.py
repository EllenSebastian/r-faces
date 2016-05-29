from __future__ import print_function

from time import time
import logging
import matplotlib.pyplot as plt

from sklearn.cross_validation import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC
from sklearn.decomposition import NMF
import pickle

def plot_gallery(images, h, w, n_row=3, n_col=4):
    """Helper function to plot a gallery of portraits"""
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        # plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())


def recompose_from_eigenfaces(X_pca,eigenfaces):
  n_examples, n_components = X_pca.shape
  X_recomposed = []
  for i in range(n_examples):
    X_recomposed.append(sum([  X_pca[i,j]*eigenfaces[j] for j in range(n_components) ]))
  return X_recomposed

# print(__doc__)
# Display progress logs on stdout
# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

lfw_people = fetch_lfw_people(min_faces_per_person=1, resize=0.4)
n_samples, h, w = lfw_people.images.shape
X, y = lfw_people.data, lfw_people.target
n_examples, n_features = X.shape

# A mapping from person to pictures that represent them
face2pics = [[]] * (max(y)+1)
for i in range(len(y)):
	face2pics[y[i]].append(i)


print("Total dataset size:")
print("n_samples: %d" % n_samples)
print("n_features: %d" % n_features)

###############################################################################
# Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
# dataset): unsupervised feature extraction / dimensionality reduction
n_components = 100
print("Extracting the top %d eigenfaces from %d faces" % (n_components, n_examples))
nmf = NMF(n_components=n_components, init='random', random_state=0).fit(X)
pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X)

nmf_components = nmf.components_.reshape((n_components, h, w))
pca_components = pca.components_.reshape((n_components, h, w))



X_nmf = nmf.transform(X)
X_pca = pca.transform(X)
print(X_nmf.shape)
print("hi")

pickle.dump( (X, X_nmf, y, nmf_components, face2pics), open( "nmfdata.p", "wb" ) )
# plot_gallery(X, h, w)
# plot_gallery(recompose_from_eigenfaces(X_nmf,nmf_components), h, w)
# # plot_gallery(recompose_from_eigenfaces(X_pca,pca_components), h, w)
# plt.show()


