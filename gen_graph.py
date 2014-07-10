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
TotalComsEnd = 100000

UserSubsDict = sql.get_subnames(TotalComsStart, TotalComsEnd)
# create dictionary assigning set of subs and count of each 
# to each user, as well as set of all subs
for i in UserSubsDict.keys():
    reddits = UserSubsDict[i]
    usersubs[i] = [set(reddits),Counter(reddits)]
    subs |= set(reddits)

min = 5 #min number of comments to be considered a 'member'

subusers = {sub:set() for sub in subs}

# Create dict with subs as keys and all users who have commented
# at least min times in a given sub as keys
# Also eliminates subreddits with no comments by given users
for sub in subs:
    for user in UserSubsDict.keys():
        if usersubs[user][1][sub] >= min:
           subusers[sub].add(user)
    if subusers[sub] == set():
       subusers.pop(sub,None)



link_min = 1
#print subusers[subusers.keys()[0]]
#print len(subusers.keys())
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
ListSubsSizes = [SubsSizes[i] for i in reddits]

SubsDescriptions = sql.get_subdata(reddits, 'description_html')
ListSubsDescriptions = [SubsDescriptions[i] for i in reddits]


sql.close()
sql.status


labels = dict()
for i in xrange(len(reddits)):
    labels[i] = reddits[i]

G = nx.to_networkx_graph(A)
nx.set_node_attributes(G,'Subreddit Name',labels)
size_dict = {i:float(ListSubsSizes[i]) for i in xrange(len(reddits))}
desc_dict = {i:str(ListSubsDescriptions[i]) for i in xrange(len(reddits))}

nx.set_node_attributes(G,'size',size_dict)
nx.set_node_attributes(G,'Descriptions',desc_dict)
nx.write_gexf(G, "test.gexf")
