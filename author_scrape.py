
import praw
import time


user_name = 'smoovewill'

r = praw.Reddit(user_agent = user_name)

thing_limit = 100
authors = []

num = 10

for i in xrange(num):
    comments = r.get_comments('all')
    for comment in comments:
        authors.append(comment.author)
    time.sleep(2)

print authors[0]
print authors[:3]
