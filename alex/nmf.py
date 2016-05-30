from time import time
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_lfw_people
from sklearn.decomposition import NMF
import pickle


# Approx 20 minutes to run
t0 = time()
n_components = 100
min_faces_per_person = 1
lfw_people = fetch_lfw_people(min_faces_per_person=min_faces_per_person, resize=0.4)
n_samples, h, w = lfw_people.images.shape
X, y, target_names = lfw_people.data, lfw_people.target, lfw_people.target_names
n_examples, n_features = X.shape
n_classes = target_names.shape[0]

# A mapping from person to pictures that represent them
# face2pics returns [n_examples X ['name',[vector of pictures indices]]}
face2pics = []
print(max(y))
for i in range((max(y)+1)):
    face2pics.append([target_names[i],[] ])
for i in range(len(y)):
    face2pics[y[i]][1].append(i)

print("Total dataset size:")
print("n_samples: %d" % n_samples)
print("n_features: %d" % n_features)
print("n_people: %d" % n_classes)


###############################################################################
# Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
# dataset): unsupervised feature extraction / dimensionality reduction
print("Extracting the top %d eigenfaces from %d faces" % (n_components, n_examples))
nmf = NMF(n_components=n_components, init='nndsvd', random_state=0, max_iter=200).fit(X)
nmf_components = nmf.components_.reshape((n_components, h, w))

print("fitting transform")
X_nmf = nmf.transform(X)

pickle.dump( (X, X_nmf, y, nmf_components, min_faces_per_person, face2pics), open( "nmfdata.p", "wb" ) )
print("done in %0.3fs" % (time() - t0))

# plot_gallery(X, h, w)
# plot_gallery(recompose_from_eigenfaces(X_nmf,nmf_components), h, w)
# # plot_gallery(recompose_from_eigenfaces(X_pca,pca_components), h, w)
# plt.show()


