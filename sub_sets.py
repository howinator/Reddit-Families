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
import sys
import sqlite3 as lite

#print repr(open('authors.csv','rb').read(200))
'''
with open("unique_copy.csv","rb") as f:
    readit = csv.reader(f)
    users = list(readit)
'''


reader = open("unique_authors.csv","r")
u  = reader.read().split('\n')
reader.close()

users = ['' for i in xrange(len(u))]


for i in xrange(len(u)):
    users[i] = u[i].strip()
        
n = 100  #number of users to consider

print users[:n]

user_name = 'smoovewill'

r = praw.Reddit(user_agent = user_name)
#dictionarywuh users as keys and set of subreddits as values
user_subs = dict()
i = 0
k = 0

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
    try:
        con = lite.connect('redditdata.db')
        
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS Comments")
        cur.execute("""CREATE TABLE Comments (total_num INT, num_4_user INT, 
            author TEXT, body TEXT, created REAL, 
            created_utc REAL, distinguished INT, downs INT, edited INT, 
            gilded INT, id TEXT, likes INT, link_author TEXT,  
            link_id TEXT, link_title TEXT, link_url TEXT, name INT, 
            num_reports INT, parent_id TEXT, subreddit_name TEXT, 
            subreddit_id TEXT, ups INT)""")
        j = 0
        for comment in comments:
            user_subs[name].add(comment.subreddit.display_name)
            SBo = comment.body
            SCr = comment.created
            SCU = comment.created_utc
            SDi = int(0 if comment.distinguished is None else 
                      comment.distinguished)
            SDo = comment.downs
            SEd = int(0 if comment.edited is False else 1)
            SGi = comment.gilded
            SId = comment.id
            SLi = int(0 if comment.likes is None else comment.likes)
            SLA = comment.link_author
            SLI = comment.link_id
            SLT = comment.link_title
            SLU = comment.link_url
            SNa = comment.name
            SNR = int(0 if comment.num_reports is None else 
                      comment.num_reports)
            SPI = comment.parent_id
            SSDN = comment.subreddit.display_name
            SSI = comment.subreddit_id
            SUp = comment.ups
            #CommTup = (k ,j, name, SBo, SCr, SCU, SDi, SDo, SEd, SGi, SId, 
            #           SLi, SLA, SLI, SLT, SLU, SNa, SPI, SSDN, SSI, SUp)
            cur.execute("""INSERT INTO Comments VALUES(?, ?, ?, ?, ?, 
                 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                 (k, j, name, SBo, SCr, SCU, SDi, SDo, SEd, SGi, SId, SLi, SLA, 
                  SLI, SLT, SLU, SNa, SNR, SPI, SSDN, SSI, SUp,))
            j += 1
            k += 1
        con.commit()
    
    except lite.Error, e:
        
        if con:
            con.rollback()
        print "Error: %s. Table not made for user: %s" % (e.args[0], user)
        sys.exit(1)
    finally:

        if con:
            con.close()
'''
#subs = set().union(*user_subs)
#generate set of subreddits
>>>>>>> Howie
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

#put subreddits with sizes in dictionary
reader = csv.reader(open('sub_sizes.csv','rb'))
sub_sizes = dict(x for x in reader)
print sub_sizes

#generate sizes for subs in graph
sizes = np.zeros(len(sub_users.keys()))
for i in xrange(len(sub_users.keys())):
    if sub_users.keys()[i] in sub_sizes.keys():
       sizes[i] = sub_sizes[sub_users.keys()[i]]
    else:
       sizes[i] = r.get_subreddit(sub_users.keys()[i]).subscribers

print np.array(sizes)
print np.log(sizes)

#generate node labels for large subreddits
labels = dict()  # ['' for i in xrange(len(sub_users.keys()))]
for i in xrange(len(sub_users.keys())):
    if sizes[i] >= 500000:
       labels[i] = sub_users.keys()[i]
       


#draw graph from A
G = nx.to_networkx_graph(A)
nx.draw_spring(G,node_size = 100* np.log(.00001*sizes),width = .05,labels = labels,font_size = 8,linewidths = 0)
plt.show()
'''
