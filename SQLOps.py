""" This class is to streamline all the operations to be done on the SQL
 database. If a new table or new operation needs to be implemented, make
 it as a new function in the class. """

# -*- coding: UTF-8 -*-

import MySQLdb as mdb
import sys
import csv

class SQLClass(object):

    def __init__(self):
        """ Re-sets return tuple to empty tuple and connects to database
        and makes cursor object for database. """

        self.data = []

    def add_comm_row(self, CUNu, UsNu, UsNa, Bo, Cr, CU, Di, Do, 
            Ed, Gi, Id, Li, LA, LI, LT, LU, Na, NR, PI, SDN, SI, Up):
        """ Adds all usable attributes from single comment returned from
        (PRAW) user.get_comments to the database. THis function must be
        called for each new comment API call. 'it' menas comment below.

        Keyword arguments:
        self -- instantiates object
        CUNu -- The comment number for this user (0 to 99)
        UsNu -- The position of the user in UserNames table (0 to total_users)
        UsNa -- The user_name for the author of it (text)
        Bo -- The text body of it (comment.body)
        Cr -- The time it was created (comment.created)
        CU -- UTC time it was created (comment.created_utc)
        Di -- If it was distinguished (comment.distinguished)
        Do -- Number of downvotes (comment.downs)
        Ed -- Was it edited? (comment.edited, 0 if False 1 if True)
        Gi -- Number of golds for comment (comment.gilded)
        Id -- id string for comment (comment.id)
        Li -- Number of liked (comment.likes)
        LA -- Author of the parent link (comment.link_author)
        LI -- id string for parent link (comment.link_id)
        LT -- Title of the parent link (comment.link_title)
        LU -- URL of the link submitted (comment.link_url)
        Na -- Name string for comment (comment.name)
        NR -- Number of times it was reported (comment.num_reports)
        PI -- id string for parent link (comment.parent_id)
        SDN -- Name of the subreddit it was posted in 
                (comment.subreddit.display_name)
        SI -- id string for subreddit it was posted in 
                (comment.subreddit_id)
        Up -- Number of upvotes for it (comment.ups) """
        
        # This snippet reads passwords from a csv.
        reader = open("mysqlargs.csv")
        passw = reader.read().split('\n')
        reader.close

        mypass = passw[1]
        Ed = int(0 if Ed is False else 1)
        NR = int(0 if NR is None else NR)

        try:

            con = mdb.connect('localhost', 'howieadmin', mypass, 'redditdata');
            # These two lines just release password sensitive data from memory.
            con.set_character_set('utf8')
            mypass = None
            passw = None
            cur = con.cursor()
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')

            
            NR = int(0 if NR is None else NR)
            cur.execute("""INSERT INTO Comments
                (num_4_user, user_num, author, body, created, created_utc, 
                distinguished, downs, edited, gilded, id, likes, link_author, 
                link_id, link_title, link_url, name, num_reports, parent_id, 
                subreddit_name, subreddit_id, ups) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (CUNu, UsNu, UsNa, Bo, 
                    Cr, CU, Di, Do, Ed, Gi, Id, Li, LA, LI, LT, LU, Na, NR, 
                    PI, SDN, SI, Up))
            con.commit()
        except mdb.Error, e:

            if con:
                con.rollback()

            print "Error %d: %s. Row not made User: %s" % (
                    e.args[0], e.args[1], UsNa)
        finally:

            if con:
                con.close()

    def get_usernames(self, start, stop):
        """ This function gets n number of usernames and returns a list
        of said usernames. """

        reader = open("mysqlargs.csv")
        passw = reader.read().split('\n')
        reader.close()

        mypass = passw[0]

        con = mdb.connect(host='howinator.homelinux.com', port=41060,user='howie',  
                passwd=mypass, db='redditdata');

        passw = None
        mypass = None
        with con:
            
            cur = con.cursor()
            cur.execute("SELECT user_name FROM UserNames")

            rows = cur.fetchall()

            names = rows[start:stop]
        nameslist = [str(i[0]) for i in names]
        return nameslist





