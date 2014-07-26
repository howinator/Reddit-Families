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

k = 100

clusters = spectral_clustering(affinity = sim,n_clusters = k)
print np.shape(clusters)

c_dict = {i:clusters[i] for i in xrange(len(clusters))}
G = nx.read_gexf('test2.gexf')
nx.set_node_attributes(G,'cluster',c_dict)
nx.write_gexf(G,'test2.gexf')


