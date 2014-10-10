import RedFams
import numpy as np
import pickle

sql = RedFams.SQLOps()
sql.open()
print sql.status
qry = 'SELECT author FROM Comments WHERE user_num < 1000'
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
print 'closed'
m = len(authorlist)
n = len(sublist)
Ratings = np.zeros((m,n))
for result in comm_counts:
    i,j = authorlist.index(result[0]),sublist.index(result[1])
    Ratings[i,j] = round(float(result[2]), 3)

pickle.dump(sublist, open('sublist.p','wb'))
pickle.dump(authorlist,open('authorlist.p','wb'))

ind = np.nonzero(Ratings)
np.save('Ratings.npy',Ratings)

