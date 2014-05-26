import csv
import MySQLdb as mdb
import sys

reader = open("unique_authors.csv","r")
u = reader.read().split('\n')
reader.close()

reader = open("mysqlargs.csv")
passw = reader.read().split("\n")
reader.close()

mypass = passw[1]

users = ['' for i in xrange(len(u))]

for i in xrange(len(u)):
    users[i] = u[i].strip()

con = mdb.connect('localhost', 'howieadmin', mypass, 'redditdata');
cur = con.cursor()

print mypass;

j = 0

for user in users:

    insert_user = "INSERT INTO UserNames(user_name) VALUES (%s)"

    cur.execute(insert_user, (user,))
    
    j += 1

con.commit()
con.close()
