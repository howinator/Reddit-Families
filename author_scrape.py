
import praw
import time
import csv

user_name = 'smoovewill'

r = praw.Reddit(user_agent = user_name)

thing_limit = 100


num = 10

for i in xrange(num):
    authors = []
    comments = r.get_comments('all')
    for comment in comments:
        authors.append(comment.author)
    
    with open('authors.csv','a') as f:
        writeit = csv.writer(f)
        for author in authors:
            writeit.writerow([author])
    time.sleep(2)

#print authors[0]
#print authors[:3]





    
