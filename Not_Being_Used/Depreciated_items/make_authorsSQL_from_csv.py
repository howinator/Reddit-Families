import csv
import sqlite3 as lite
import sys

reader = open("unique_authors.csv","r")
u = reader.read().split('\n')
reader.close()

users = ['' for i in xrange(len(u))]

for i in xrange(len(u)):
    users[i] = u[i].strip()

con = lite.connect('redditdata.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS UserNames")
cur.execute("CREATE TABLE UserNames (user_number INT, user_name TEXT)")

j = 0

for user in users:
    inp = (j, user,)

    cur.execute("""INSERT INTO UserNames VALUES(?, ?)""", inp)
    
    j += 1

con.commit()
con.close()
