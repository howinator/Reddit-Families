import RedFams
import praw
import time
import sys

# -*- coding: UTF-8 -*-

agent = 'Subreddit scraping script by /u/howinator'

r = praw.Reddit(user_agent = agent)
sql = RedFams.SQLOps()
sql.open()
print sql.status

strt = 0
end = 499

subs = set([])

for user in xrange(500):
    sub = sql.get_usersubs(user)
