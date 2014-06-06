import RedFams
import praw
import time
import sys

# -*- coding: UTF-8 -*-

agent = 'Subreddit scraping script by /u/howinator'

r = praw.Reddit(user_agent = agent)

sql = RedFams.SQLOps()
sql.open()

# Starting and ending point for comment pulling
CommentsStart = 0
CommentsEnd = 5000

# Get dictionary of user keys and subreddit names as lists for value
UserSubsDict = sql.get_subnames(CommentsStart, CommentsEnd)

SubsSet = set()
# Add all subreddits to a set in order to remove values
for i in UserSubsDict.keys():
    reddits = UserSubsDict[i]
    SubsSet |= set(reddits)

m = 0
for sub in SubsSet:
    print m
    m += 1
    try:
        s = r.get_subreddit(sub)
        sql.add_sub_row(s.accounts_active, s.comment_score_hide_mins,
                s.created, s.created_utc, s.description, s.description_html,
                s.display_name, s.has_fetched, s.header_img, s.header_title,
                s.id, s.json_dict, s.name, s.over18, s.public_description,
                s.public_traffic, s.submission_type, s.submit_link_label,
                s.submit_text, s.submit_text_html, s.submit_text_label,
                s.subreddit_type, s.subscribers, s.title, s.url)

    except praw.requests.HTTPError:
        print sub,'does not exist'

sql.close()
