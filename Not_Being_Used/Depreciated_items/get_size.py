import csv
import praw


reader = open('unique_authors.csv','r')
u = reader.read().split('\n')
reader.close()

users = ['' for i in xrange(len(u))]

for i in xrange(len(u)):
    users[i] = u[i].strip()

subs = set([])

user_name = 'smoovewill'
r = praw.Reddit(user_agent = user_name)

n = 100
i = 0
for name in users[:n]:
    print i
    i += 1
    user = r.get_redditor(name)
    comments = user.get_comments(limit=100)
    for comment in comments:
        subs.add(comment.subreddit.display_name)
print len(subs)
print subs


i = 0
sub_size = dict()
for sub in subs:
    print i
    i+=1
    sub_size[sub] = r.get_subreddit(sub).subscribers

writer = csv.writer(open('sub_sizes.csv', 'wb'))
for key, value in sub_size.items():
     writer.writerow([key, value])









