import numpy as np
import networkx as nx
from sklearn.cluster import spectral_clustering
from sklearn.preprocessing import normalize
import pickle

R = np.load('Ratings.npy')
subs = pickle.load(open('sublist.p','rb'))
R = normalize(R,axis=0)
print 'sizes'

sim = np.dot(np.transpose(R),R)

k = 10

clusters = spectral_clustering(sim,n_clusters = k)
print clusters
print len(clusters)
print type(clusters)
