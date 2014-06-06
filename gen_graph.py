import RedFams
from collections import Counter
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

sql = RedFams.SQLOps()
sql.open()
print sql.status

subs = set()

usersubs = dict()

TotalComsStart = 0
TotalComsEnd = 10000

UserSubsDict = sql.get_subnames(TotalComsStart, TotalComsEnd)

for i in UserSubsDict.keys():
    reddits = UserSubsDict[i]
    usersubs[i] = [set(reddits),Counter(reddits)]
    subs |= set(reddits)

min = 20 #min number of comments to be considered a 'member'

subusers = {sub:set() for sub in subs}

for sub in subs:
    for user in UserSubsDict.keys():
        if usersubs[user][1][sub] >= min:
           subusers[sub].add(user)
    if subusers[sub] == set():
       subusers.pop(sub,None)



link_min = 2
#print subusers[subusers.keys()[0]]
print len(subusers.keys())
A = np.zeros((len(subusers.keys()),len(subusers.keys())))
reddits = subusers.keys()
for i in xrange(len(reddits)):
    for j in xrange(i,len(reddits)):
        # Intersection of subreddit_i and subreddit_j 
        common = len(subusers[reddits[i]]&subusers[reddits[j]])
        if common >= link_min:
           A[i,j] = common
           A[j,i] = A[i,j]

SubsSizes = sql.get_subsize(reddits)
ListSubsSizes = SubsSizes.values()
print ListSubsSizes
min_size = np.array([.5 for i in xrange(len(reddits))])
node_sizes = np.maximum(np.log(ListSubsSizes),min_size)
sql.close()
sql.status

labels = dict()
for i in xrange(len(reddits)):
    if node_sizes[i] >= 5:
       labels[i] = reddits[i]
    else:
       labels[i] = ''

G = nx.to_networkx_graph(A)
nx.draw(G,node_size = node_sizes,labels = labels,
        font_size = 8,width = .5,linewidths = 0.5)
plt.show()
nx.write_gexf(G, "test.gexf")
