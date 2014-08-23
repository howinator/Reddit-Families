import pickle
import RedFams
import string
from stemming.porter2 import stem
import numpy as np
import matplotlib.pyplot as plt

subs = pickle.load(open('sublist.p','rb'))[:50]
sql = RedFams.SQLOps()
sql.open()
print sql.status
qry = '''SELECT DISTINCT subreddit_name, link_title
         FROM Comments
         WHERE subreddit_name IN %s'''

results = sql.query(qry,[subs])
sql.close()
print sql.status

sub_titles = {sub:[] for sub in subs}

titles = [result[1] for result in results]
titles = list(set(titles))
title_string = ''.join(titles).lower()
punct = set(string.punctuation)
print 'stripping punctuation'
title_string = ''.join(c for c in title_string if c not in punct)
title_wordlist = title_string.split()

with open('stopwords.txt','rb') as f:
     s = f.read()
     stopwords = s.split('\n')
print s
print 'removing stopwords'
title_wordlist = [word for word in title_wordlist if word not in stopwords]
print title_wordlist[:100]


with open('english_words.txt','rb') as f:
     s=f.read()
     masterlist = s.split('\n')


masterlist = [s.lower() for s in masterlist]

print len(title_wordlist), 'words'

wordset = set(masterlist) & set(title_wordlist)

title_wordlist = [word for word in title_wordlist if len(word) == 1 or word in wordset]
print len(title_wordlist), 'words after dict matching'

print title_wordlist[:100]

print 'stemming'
for i in xrange(len(title_wordlist)):
    title_wordlist[i] = stem(title_wordlist[i])

print len(title_wordlist)
print title_wordlist[:100]
wordcounts = dict()
for word in title_wordlist:
    if word not in wordcounts.keys():
       wordcounts[word] = title_wordlist.count(word)
print wordcounts

print max(wordcounts.values())

x_data = range(2,max(wordcounts.values())+1)
y_data = [0 for i in xrange(len(x_data))]
for word in wordcounts.keys():
    if wordcounts[word] > 1:
       y_data[wordcounts[word]-2] += 1


plt.plot(np.array(x_data),np.array(y_data))
plt.show()
    





