import praw
import pickle

#This will be a computationalthings account in the future
user =  ''
r = praw.Reddit(user_agent = user)
password = ''
r.login(user,password)


suggestions = pickle.load(open('user_suggestions.p'))
authors = pickle.load(open('authorlist.p'))

messages = ['' for i in xrange(len(authors))]

for i in xrange(len(authors)):
    msg = 'Hi',authors[i],'''!  This is Sarang and Howie from 
          computationalthings.com!  You can read about what we're doing 
          at our website, but basically, we want to make you some subreddit
          suggestions based on your commenting activity.  

          Based on the subreddits you've commented on in the past, we'd like
          to suggest you check out the following subreddits:'''
    
    msg += '\n' 
    
    for sub in suggestions[authors[i]]:
        msg += '/r/' + sub +'\n'

    msg += '''Thanks for reading this.  Please feel free to comment on our
              blog or reply to this message with any feedback/suggestions.  We
              hope this has been useful to you.

              Best,

              Howie and Sarang'''

    r.send_message(authors[i],'Some subreddit suggestions for you!', msg)







