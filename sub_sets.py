#This script takes the author list, generates the subreddits they comment
#in, and generates and draws a graph where the nodes are subreddits
#and connections are made when a user has a comment in two subreddits
#you'll need networkx (you can just sudo pip install networkx)
import csv
import praw
import numpy as np
import time
import networkx as nx
from matplotlib import pyplot as plt
from tempfile import TemporaryFile

numpy_saved = TemporaryFile()

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
        
<<<<<<< HEAD
n = 10  #number of users to consider
=======
n = 8000  #number of users to consider
>>>>>>> 4617a06375b3ed29ac2d184881dbd816f6ae05cc

print users[:n]

user_name = 'smoovewill'

r = praw.Reddit(user_agent = user_name)

#dictionarywuh users as keys and set of subreddits as values
user_subs = dict()
i = 0
j = 0


#generate dict of users and sets of subreddits
for name in users[:n]:
    print i
    i += 1
    user = r.get_redditor(name)
    user_subs[name] = set([])
    # So, right here I changed it so that the object was instantiated
    # before the loop was started. I also took out the sleep command
    # because I learned PRAW takes care of the API limit. -Howie
    comments = user.get_comments(limit = 100)
    for comment in comments:
        user_subs[name].add(comment.subreddit.display_name)
        
        # 'distinguished', 'likes', 'num_reports' may be NoneTypes, so they
        # must be converted to int
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
print 'max weight is', np.amax(A)


#generate node sizes based on subreddit sizes
sizes = np.zeros(len(sub_users.keys()))
for i in xrange(len(sub_users.keys())):
    sizes[i] = r.get_subreddit(sub_users.keys()[i]).subscribers

print np.array(sizes)
print 10* np.log(.01*sizes)

#generate node labels for large subreddits
labels = dict()  # ['' for i in xrange(len(sub_users.keys()))]
for i in xrange(len(sub_users.keys())):
    if sizes[i] >= 1000000:
       labels[i] = sub_users.keys()[i]
       


#draw graph from A
G = nx.to_networkx_graph(A)
nx.draw_spring(G,node_size = 100* np.log(.00001*sizes),width = .05,labels = labels,font_size = 8,linewidths = 0)
plt.show()

