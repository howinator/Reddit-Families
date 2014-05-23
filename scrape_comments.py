import SQLOps
import csv
import praw
import time
import sys

agent = 'Comment scraping script by /u/howinator'

r = praw.Reddit(user_agent = agent)

NUsersStart = 1332
NUsersStop = 20000

sql = SQLOps.SQLClass()

authors = sql.get_usernames(NUsersStart, NUsersStop)

i = 0
k = 0
# This is just to find the starting point for the script.
m = NUsersStart

print users

for name in users:
    print m

    user = r.get_redditor(name)
    comments = user.get_comments(limit = 100)

    j = 0

    for comment in comments:
        sql.add_comm_row(k, j, m, name, comment.body, comment.created, 
                comment.created_utc, comment.distinguished, comment.downs, 
                comment.edited, comment.gilded, comment.id, comment.likes, 
                comment.link_author, comment.link_id, comment.link_title, 
                comment.link_url, comment.name, comment.num_reports, 
                comment.parent_id, comment.subreddit.display_name, 
                comment.subreddit_id, comment.ups)
        
        j += 1
        k += 1
    m += 1
