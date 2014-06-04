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

subs = set()

for user in xrange(500):
    # Gets all subreddits for this user_num
    user_subs = sql.get_usersubs(user)
    # Adds unique user_subs to subs
    subs |= set(user_subs)

total_num_subs = len(subs)
print total_num_subs

j = 0

for sub in subs:
    try:
        s = r.get_subreddit(sub)
        sql.add_sub_row(j, sub, s.accounts_active, s.comment_score_hide_mins, 
            s.created, s.created_utc, s.description, s.desscription_html, 
            s.has_fetched, s.header_img, s.header_size, s.header_title, 
            s.id, s.name, s.over18, s.public_description, s.public_traffic, 
            s.submission_type, s.submit_text, s.submit_text_html, 
            s.submit_text_label, s.subreddit_type, s.subscribers, s.title, 
            s.url)
        j += 1
    except praw.requests.HTTPError:
        print sub,'does not exist'

sql.close()`
