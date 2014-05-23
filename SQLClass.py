""" This class is to streamline all the operations to be done on the SQL
 database. If a new table or new operation needs to be implemented, make
 it as a new function in the class. """

import sqlite3 as lite

class SQLOps(object):

    def __init__(self):
        """ Re-sets return tuple to empty tuple and connects to database
        and makes cursor object for database. """

        self.data = ()
        con = lite.connect('redditdata.db')
        cur = con.cursor

    def add_comm_row(self, ToNu, UsNu, UsNa, Bo, Cr, CU, Di, Do, 
            Ed, Gi, Id, Li, LA, LI, LT, LU, Na, NR, PI, SDN, SI, Up):
        """ Adds all usable attributes from single comment returned from
        (PRAW) user.get_comments to the database. THis function must be
        called for each new comment API call. 'it' menas comment below.

        Keyword arguments:
        self -- instantiates object
        ToNu -- The total number for this comment (0 to total_authors*100)
        UsNu -- The comment number for this user (0 to 99)
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

        try:
            Ed = int(0 if Ed is False else 1)
            NR = int(0 if NR is None else NR)
            cur.execute("""INSERT INTO Comments VALUES(?, ?, ?, ?, ?, ?, 
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (ToNu, UsNu, UsNa, Bo, Cr, CU, Di, Do, Ed, Gi, Id, Li, 
                 LA, LI, LT, LU, Na, NR, PI, SDN, SI, Up,))
            con.commit()
        except lite.Error, e:

            if con:
                con.rollback()

            print "Error %s. Row not made for comment No: %s, User: %s" % (
                    e.args[0], ToNu, UsNa)
        finally:

            if con:
                con.close()




