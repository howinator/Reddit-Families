#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import praw
user_agent = ("Subreddit Families 0.0.1 by /u/Howinator")
r = praw.Reddit(user_agent=user_agent)
thing_limit = 100
comments = r.get_comments('all', gilded_only=False, limit=thing_limit)
authors = []
for comment in comments:
    authors.append(comment.author)

print(authors[0].name)








#user_name = "Howinator"
#user = r.get_redditor(user_name)
#gen = user.get_submitted(limit=thing_limit)
#karma_by_subreddit = {}
#for thing in gen:
#  subreddit = thing.subreddit.display_name
#  karma_by_subreddit[subreddit]= (karma_by_subreddit.get(subreddit, 0) + thing.score)
