import SQLOps
import csv
import praw
import time
import sys

agent = 'Comment scraping script by /u/howinator'

r = praw.Reddit(user_agent = agent)

NUsersStart = 0
NUsersStop = 16000

sql = SQLOps.SQLClass()

users = sql.get_usernames(NUsersStart, NUsersStop)

i = 0
k = 0
# This is just to find the starting point for the script.
m = NUsersStart


# fix this later.
users = authors

print users



for name in users:
    print m
    try:
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
    except praw.requests.HTTPError:
        print name,'does not exist'
         
