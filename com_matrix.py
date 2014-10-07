import RedFams
import numpy as np
import pickle

sql = RedFams.SQLOps()
sql.open()
print sql.status
qry = 'SELECT author FROM Comments'
authors = sql.query(qry)
authortuple = tuple(author[0] for author in authors)
authorlist = list(set(authortuple))

qry = 'SELECT subreddit_name FROM Comments WHERE author IN %s'
subs = sql.query(qry,[authorlist])
sublist = list(set([sub[0] for sub in subs]))   

qry = '''SELECT author, subreddit_name, count(id) FROM Comments
         WHERE author IN %s AND subreddit_name IN %s
         GROUP BY author, subreddit_name'''


comm_counts = sql.query(qry,[authorlist,sublist])
sql.close()
print 'closed'
m = len(authorlist)
n = len(sublist)
Ratings = np.zeros((m,n))
k = 0
for result in comm_counts:
    i,j = authorlist.index(result[0]),sublist.index(result[1])
    Ratings[i,j] = int(result[2])
    if k % 1000== 0:
        print "\n\nIteration number: " + str(k) + "\n"
    k += 1
'''    
for i in xrange(m):
    for j in xrange(n):
        for result in comm_counts:
            if result[0] == authorlist[i] and result[1] == sublist[j]:
               Ratings[i,j] = float(result[2])
'''

pickle.dump(sublist, open('sublist.p','wb'))
pickle.dump(authorlist,open('authorlist.p','wb'))

ind = np.nonzero(Ratings)
np.save('Ratings.npy',Ratings)

