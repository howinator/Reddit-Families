import numpy as np
import networkx as nx
import RedFams
from sklearn.preprocessing import normalize
from matplotlib import pyplot as plt

R = np.load('Ratings.npy')
R = normalize(R, axis = 0)

m,n = np.shape(R)

# Compute weighted adjacency
A = np.dot(np.transpose(R),R)

G = nx.to_networkx_graph(A)
nx.draw_networkx(G)
plt.show()


