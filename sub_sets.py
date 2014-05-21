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
        
n = 1  #number of users to consider

print users[:n]

user_name = 'smoovewill'

r = praw.Reddit(user_agent = user_name)

#dictionarywuh users as keys and set of subreddits as values
user_subs = dict()
i = 0
j = 0

''' 
Here the numpy array with all the info on the retrieved comments is
instantiated. NOTE: every 100 entired will be of the same author.
As far as I can tell, structured numpy arrays can't have one dimension that
is of a different size. Info on structured arrays can be found here:
http://docs.scipy.org/doc/numpy/user/basics.rec.html
'''
CommInfo = np.zeros((n*100,),dtype={'names':['user_name', 'body', 
    'created', 'created_utc', 'distinguished', 'downs', 'edited', 
    'gilded', 'id', 'likes', 'link_author', 'link_id', 'link_title',
    'link_url', 'name', 'num_reports', 'parent_id', 
    'subreddit_name', 'subreddit_id', 'ups'], 
    'formats':['U20', 'U10000', 'f8', 'f8', 'i4', 'i4', 'b', 'i4', 'U12', 
        'i4', 'U20', 'U12', 'U300', 'U200', 'U16', 'i4', 'U16', 'U100',
        'U16', 'i4'
  ]})
NuUNa = CommInfo['user_name']
NuBo = CommInfo['body']
NuCr = CommInfo['created']
NuCrU = CommInfo['created_utc']
NuDi = CommInfo['distinguished']
NuDo = CommInfo['downs']
NuEd = CommInfo['edited']
NuGi = CommInfo['gilded']
NuId = CommInfo['id']
NuLik = CommInfo['likes']
NuLiA = CommInfo['link_author']
NuLiI = CommInfo['link_id']
NuLiT = CommInfo['link_title']
NuLiU = CommInfo['link_url']
NuNa = CommInfo['name']
NuNu = CommInfo['num_reports']
NuPa = CommInfo['parent_id']
NuSuN = CommInfo['subreddit_name']
NuSuI = CommInfo['subreddit_id']
NuUp = CommInfo['ups']

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
        ChDi = int(0 if comment.distinguished is None else 
                comment.distinguished)
        ChLi = int(0 if comment.likes is None else comment.likes)
        ChNuR = int(0 if comment.num_reports is None else 
                comment.num_reports)
        # Here I populate the numpy array.
        NuUNa[j] = name
        NuBo[j] = comment.body
        NuCr[j] = comment.created
        NuCrU[j] = comment.created_utc
        NuDi[j] = ChDi
        NuDo[j] = comment.downs
        NuEd[j] = comment.edited
        NuGi[j] = comment.gilded
        NuId[j] = comment.id
        NuLik[j] = ChLi
        NuLiA[j] = comment.link_author
        NuLiI[j] = comment.link_id
        NuLiT[j] = comment.link_title
        NuLiU[j] = comment.link_url
        NuNa[j] = comment.name
        NuNu[j] = ChNuR
        NuPa[j] = comment.parent_id
        NuSuN[j] = comment.subreddit.display_name
        NuSuI[j] = comment.subreddit_id
        NuUp[j] = comment.ups
        
        j += 1
print NuBo[:]
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

