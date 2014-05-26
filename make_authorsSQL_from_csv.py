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

j = 0

for i in xrange(len(u)):
    users[i] = u[i].strip()
    j += 1

# Without this, thie last row od the csv was blank.
users = users[:(j-1)]    

con = mdb.connect('localhost', 'howieadmin', mypass, 'redditdata');
cur = con.cursor()

# These two li8nes just clear the variables from memory to prevent intrusions.
mypass = None
passw = None

cur.execute("DROP TABLE IF EXISTS UserNames")
cur.execute("""CREATE TABLE UserNames(user_num INT PRIMARY KEY AUTO_INCREMENT, 
        user_name TEXT)""")

for user in users:

    insert_user = "INSERT INTO UserNames(user_name) VALUES (%s)"

    cur.execute(insert_user, (user,))

con.commit()
con.close()
