import RedFams
import praw
import time
import sys

# -*- coding: UTF-8 -*-

agent = 'Subreddit scraping script by /u/howinator'

r = praw.Reddit(user_agent = agent)

strt = 0
end = 499

userlist = sql.get_usernames(strt, end)

subs = set([])

for
