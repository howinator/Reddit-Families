#This scripttakes the author list, generates the subreddits they comment
#in, and generates and draws a graph where the nodes are subreddits
#and connections are made when a user has a comment in two subreddits
#you'll need networkx (you can just sudo pip install networkx)
import csv
import praw
import numpy as np
import time
import networkx as nx
from matplotlib import pyplot as plt

#print repr(open('authors.csv','rb').read(200))
'''
with open("unique_copy.csv","rb") as f:
    readit = csv.reader(f)
    users = list(readit)
'''


reader = open("authors.csv","r")
u  = reader.read().split('\n')
reader.close()

users = ['' for i in xrange(len(u))]


for i in xrange(len(u)):
    users[i] = u[i].strip()
    
    
n = 10  #number of users to consider

print users[:n]



user_name = 'smoovewill'


r = praw.Reddit(user_agent = user_name)

#dictionarywuh users as keys and set of subreddits as values
user_subs = dict()
i = 0
#generate dict of users and sets of subreddits
for name in users[:n]:
    print i
    i += 1
    user = r.get_redditor(name)
    user_subs[name] = set([])
    for comment in user.get_comments():
        user_subs[name].add(comment.subreddit.display_name)
        time.sleep(2)
        
             
#subs = set().union(*user_subs)
#generate set of subreddits
subs = set([])
for name in user_subs.keys():
    subs |= user_subs[name]


print len(subs)
print subs

#generate dict with subreddit as keys and set of users as values
sub_users = dict()
for sub in subs:
    sub_users[sub] = set([])
    for name in users[:n]:
        if sub in user_subs[name]:
          sub_users[sub].add(name)

#A is the adjacency matrix
A = np.zeros((len(subs),len(subs)))

#generate adjacency matrix (weighted) 
for i in xrange(len(sub_users.keys())):
    for j in xrange(i,len(sub_users.keys())):
        A[i,j] += len(sub_users[sub_users.keys()[i]]&sub_users[sub_users.keys()[j]])
        A[j,i] = A[i,j]

print A

#draw graph from A
G = nx.to_networkx_graph(A)
nx.draw(G)
plt.show()



