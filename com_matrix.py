import RedFams
import numpy as np


sql = RedFams.SQLOps()
sql.open()
qry = 'SELECT author FROM Comments WHERE user_num < 500'
authors = sql.query(qry)
authortuple = tuple(author[0] for author in authors)
authorlist = list(set([author[0] for author in authors]))
#print authorlist

qry = 'SELECT subreddit_name FROM Comments WHERE author IN %s'
subs = sql.query(qry,[authorlist])
sublist = list(set([sub[0] for sub in subs]))   
#print sublist

qry = '''SELECT author, subreddit_name, count(author) FROM Comments
         WHERE author IN %s AND subreddit_name IN %s
         GROUP BY author'''

comm_counts = sql.query(qry,[authorlist,sublist])
sql.close()

m = len(authorlist)
n = len(sublist)
print m,n
Ratings = np.zeros((m,n))
for i in xrange(m):
    for j in xrange(n):
        for result in comm_counts:
            if result[0] == authorlist[i] and result[1] == sublist[j]:
               Ratings[i,j] = float(result[2])


print np.amax(Ratings)
print Ratings
ind = np.nonzero(Ratings)
print len(ind[0]), len(ind[1])
print Ratings[ind]
