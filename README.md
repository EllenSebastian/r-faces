# r-faces
Using R-trees to store and query faces.

installation: 

download libspatialindex from http://libspatialindex.github.io/#download
download Rtree from https://pypi.python.org/pypi/Rtree/
cd libspatialindex-src-1.8.5
./configure; make; make install
cd Rtree-0.8.2
python setup.py install