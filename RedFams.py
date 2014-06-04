""" This class is to streamline all the operations to be done on the SQL
 database. If a new table or new operation needs to be implemented, make
 it as a new function in the class. """

# -*- coding: UTF-8 -*-

import MySQLdb as mdb
import sys
import csv

class SQLOps(object):
    """ This class is to streamline all the operations to be done on the SQL
    database. Each new operation on the database should be implemented as a 
    new method. """

    def __init__(self):
        """ Re-sets the connection to the closed state"""
        self.status = 'closed'

    def __enter__(self):
        """This method enables the use of a with statement by calling open. """
        self.open()
        return self

    def __exit__(self, type, value, tb):
        """This method handles errors by calling close. """
        self.close()
    
    def open(self):
        """This method reads the password for the database and then makes 
        the connection. """
        reader = open('mysqlargs.csv')
        passw = reader.read().split('\n')
        reader.close()
        mypass = passw[0]
        self.con = mdb.connect(host="mysql.computationalthings.com", 
                user="howieadmin", passwd = mypass, db="redditdata")
        passw = None
        mypass = None
        self.con.set_character_set('utf8')
        self.status = "open"

    def close(self):
        " Simply calls the MySQLdb close method to close connection. "
        self.con.close()
        self.status = "closed"

    def get_usernames(self, start, stop):
        """Gets (stop-start) number of usernames and returns list."""
        cur = self.con.cursor()
        cur.execute("SELECT user_name FROM UserNames")

        rows = cur.fetchall()

        names = rows[start:stop]
        # This next line converts the list of singular tuples into a list of
        # strings.
        nameslist = [str(i[0]) for i in names]
        return nameslist

    def get_usersubs(self, num):
        """Gets subreddit names when the author matches the name parameter."""
        cur = self.con.cursor()
        cur.execute("SELECT subreddit_name FROM Comments WHERE total_num <= 42386 && user_num = %s",
                (num,))
        subs = cur.fetchall()

        # Again converts tuple into string.
        sub_list = [i[0] for i in subs]
        return sub_list

    def get_info(self):
        """ Gets info about the tables. """
        cur.self.con.cursor()
        cur.execute("SHOW TABLES")

        cur.execute("SHOW COLUMNS FROM Comments")
        return cur.fetchall()



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


        cur = self.con.cursor()
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
        self.con.commit()

