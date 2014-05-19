import csv
import praw
import numpy as np
import time

#print repr(open('authors.csv','rb').read(200))

with open("unique_copy.csv","rb") as f:
    readit = csv.reader(f)
    users = list(readit)

'''
reader = open("authors.csv","r")
users  = reader.read().split('\n')
reader.close()
'''

user_name = 'smoovewill'


r = praw.Reddit(user_agent = user_name)

user_subs = dict()
for user_name in users[:10]:
    user = r.get_redditor(user_name)
    user_subs[user_name] = set([])
    for comment in user.get_comments():
        user_subs[user_name].add(comment.subreddit)
        time.sleep(2)
    time.sleep(2)    
             
subs = set().union(*user_subs)

print len(subs)
print subs


