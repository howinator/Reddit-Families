import SQLOps
from collections import Counter
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


sql = SQLOps.read_SQL()
sql.open()
print sql.status

strt = 0
end = 50

userlist = sql.get_usernames(strt,end)
usersubs = dict()
subs = set()
for user in userlist:
    reddits = sql.get_usersubs(user)
    usersubs[user] = [set(reddits),Counter(reddits)]
    subs |= set(reddits)
    

sql.close()
print sql.status

min = 5 #min number of comments to be considered a 'member'

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


G = nx.to_networkx_graph(A)
nx.draw_networkx(G,node_size = 50,with_labels = False,width = .5,linewidths = 0)
plt.show()




    
