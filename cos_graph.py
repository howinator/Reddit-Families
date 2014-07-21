import numpy as np
import networkx as nx
import RedFams
from sklearn.preprocessing import normalize
from matplotlib import pyplot as plt
import pickle

R = np.load('Ratings.npy')
R = normalize(R, axis = 0)
sublist = pickle.load(open('sublist.p','rb'))
authorlist = pickle.load(open('authorlist.p','rb'))
m,n = np.shape(R)

# Compute weighted adjacency
A = np.dot(np.transpose(R),R)

sql = RedFams.SQLOps()
sql.open()
qry = '''SELECT display_name,url,subscribers,over18,header_title,title
         FROM Subreddits
         WHERE display_name IN %s
         GROUP BY display_name'''

data = sql.query(qry,[sublist])
urldict = dict()
sizedict = dict()
NSFWdict = dict()
titledict = dict()
for i in xrange(len(data)):
    j = sublist.index(data[i][0])
    urldict[j] = str(data[i][1])
    sizedict[j] = float(data[i][2])
    if data[i][3] == 1:
       NSFWdict[j] = 'NSFW'
    else:
       NSFWdict[j] = 'SFW'
    titledict[j] = str(data[i][5])

namedict = {i:str(sublist[i]) for i in xrange(len(sublist))}

#print data
sql.close()
G = nx.to_networkx_graph(A)
nx.set_node_attributes(G,'Subreddit name',namedict)
nx.set_node_attributes(G,'size',sizedict)
nx.set_node_attributes(G,'url',urldict)
nx.set_node_attributes(G,'NSFW',NSFWdict)
#nx.set_node_attributes(G,'title',titledict)

nx.write_gexf(G,"test2.gexf")

#nx.draw_networkx(G)
#plt.show()


