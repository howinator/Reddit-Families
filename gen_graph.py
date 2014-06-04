import RedFams
from collections import Counter
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

sql = RedFams.SQLOps()
sql.open()
print sql.status

strt = 0
end = 1

userlist = range(strt,end)
usersubs = dict()
subs = set()
for user in userlist:
    reddits = sql.get_usersubs(user)
    usersubs[user] = [set(reddits),Counter(reddits)]
    subs |= set(reddits)
    

sql.close()
print sql.status

min = 20 #min number of comments to be considered a 'member'

subusers = {sub:set() for sub in subs}
for sub in subs:
    for user in userlist:
        if usersubs[user][1][sub] >= min:
           subusers[sub].add(user)
    if subusers[sub] == set():
       subusers.pop(sub,None)




#print subusers[subusers.keys()[0]]
print len(subusers.keys())
A = np.zeros((len(subusers.keys()),len(subusers.keys())))
reddits = subusers.keys()
for i in xrange(len(reddits)):
    for j in xrange(i,len(reddits)):
        A[i,j] += len(subusers[reddits[i]]&subusers[reddits[j]])
        A[j,i] = A[i,j]

min_size = np.array([.5 for i in xrange(len(reddits))])
node_sizes = np.maximum(50*np.log(.05*np.sum(A,axis=1)),min_size)


labels = dict()
for i in xrange(len(reddits)):
    if node_sizes[i] >= 25:
       labels[i] = reddits[i]
    else:
       labels[i] = ''

G = nx.to_networkx_graph(A)
nx.draw_spring(G,node_size = node_sizes,labels = labels,font_size = 8,width = .05,linewidths = 0.05)
plt.show()




    
