import RedFams
import numpy as np


sql = RedFams.SQLOps()
sql.open()
print sql.status
qry = 'SELECT author FROM Comments WHERE user_num < 100'
authors = sql.query(qry)
authortuple = tuple(author[0] for author in authors)
authorlist = list(set(authortuple))

qry = 'SELECT subreddit_name FROM Comments WHERE author IN %s'
subs = sql.query(qry,[authorlist])
sublist = list(set([sub[0] for sub in subs]))   

qry = '''SELECT author, subreddit_name, count(*) FROM Comments
         WHERE author IN %s AND subreddit_name IN %s
         GROUP BY author, subreddit_name
         ORDER BY author'''


comm_counts = sql.query(qry,[authorlist,sublist])
sql.close()
m = len(authorlist)
n = len(sublist)
Ratings = np.zeros((m,n))
for i in xrange(m):
    for j in xrange(n):
        for result in comm_counts:
            if result[0] == authorlist[i] and result[1] == sublist[j]:
               Ratings[i,j] = float(result[2])


ind = np.nonzero(Ratings)
np.save('Ratings.npy',Ratings)

