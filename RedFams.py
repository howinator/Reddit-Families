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
     
    def query(self, qry):
        '''Gives us more flexibility, this will just take any SQL 
        query string qry and execute and return it'''
        cur = self.con.cursor()
        cur.execute(qry)
        result = cur.fetchall()
        return result


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

    def get_subsize(self, Subs):
        """Takes a list of subreddits as the argument, and returns a dictionary
        with the number of subscribers for the subreddit. 
        NOTE: Value of 0.1 means that there as an error with that subreddit."""

        cur = self.con.cursor()
        SubsSize = dict()

        # This just fetches the subreddits' subscribers one-by-one
        for sub in Subs:
            if sub == None:
                SubsSize[sub] = 0
            else:
                cur.execute("""SELECT subscribers FROM Subreddits 
                    WHERE display_name = %s""", (sub,))
                TupleSubscribers = cur.fetchall()
                # Converts from long int to regular int
                ListSubscribers = [float(i[0]) if i[0] != None else 0.1 
                        for i in TupleSubscribers]
                # checks for empty list
                SubsSize[sub] = 0.1 if not ListSubscribers else \
                                ListSubscribers[0]
        print SubsSize
        return SubsSize
    
    
    def get_subdata(self,subs,cols):
        '''
        This takes a list (or single) of subreddits (column names) and returns
        a dictionary with each key being a subreddit and the values being list
        of data corresponding to the column names provided.  There are probably 
        ways to optimize this.
        '''

        if type(subs) == type(''):
           subs = [subs]
        if type(cols) == type(''):
           cols = [cols]
           
        cur = self.con.cursor()
        data = dict()
        col_names = ",".join(cols)
        print col_names
        for sub in subs:
            query = "SELECT " + col_names + """ FROM Subreddits WHERE 
                 display_name = %s"""
            print query
            cur.execute(query, (sub,))
            lst = list(cur.fetchone())
            dic = {cols[i]:lst[i] for i in xrange(len(cols))}
            data[sub] = dic
        return data

    def get_subnames(self, TotStart, TotEnd):
        """Gets subreddit names for users that have total_num corresponding to
        tot_start and tot_end. It gets redditors who are completely 
        contained between tot_start and tot_end by  return comments for
        user_num - 1. The redditor who has a comment at tot_end may have 
        comments who are after tot_end. It returns a dictionary where the 
        key is user_num and the value is a list of subreddit_names."""

        cur = self.con.cursor()
        UsersSubs = dict()

        cur.execute("""SELECT user_num FROM Comments WHERE total_num >= %s AND 
                     total_num < %s""", (TotStart, TotEnd))
        TupleUserNums = cur.fetchall()

        # This comprehension converts the tuple from cur.fetchall() into list
        # int() is there because mysql appends L to value because it returns
        # python Long Int
        UserNumList = [int(i[0]) for i in TupleUserNums]
        
        # This forms a list with only unique user numbers and preserves order
        UniqueUserNumList = []
        for i in UserNumList:
            if i not in UniqueUserNumList:
                UniqueUserNumList.append(i)

        FirstUser = UniqueUserNumList[0]
        LastFullUser = UniqueUserNumList[-2]

        cur.execute("""SELECT user_num, subreddit_name FROM Comments 
            WHERE total_num >= %s AND total_num < %s 
            AND user_num >= %s AND user_num < %s""", (TotStart, TotEnd, 
                FirstUser, LastFullUser))

        # This little Charlie Foxtrot right here builds the UserSubs dictionary
        # keeping user, subreddit pairs sorted correctly.
        
        UserSubsList = []
        j = 0
        for i in range(cur.rowcount):
            row = cur.fetchone()

            # Just to get into the next if statement on the first iteration
            if i == 0:
                user_i = row[0]

            user_ipl1 = row[0]

            if user_i == user_ipl1:
                UserSubsList.append(row[1])
            else:
                user_i = int(user_i)
                UsersSubs[user_i] = UserSubsList
                UserSubsList = []
                UserSubsList.append(row[1])
                user_i = user_ipl1
  
        return UsersSubs 

    def get_info(self):
        """ Gets info about the tables. """
        cur = self.con.cursor()
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

    def add_sub_row(self, Ac, ScHd, Cr, CrUt, Dn, DnHl, 
            DsNm, HF, HImg, HdTl, Id, JSON, Na, NSFW, 
            PuDn, PbTr, ST, SLL, STex, STexH, STexL, SbTp, Size, Tl, URL):
        """ Adds all usable attributes from single comment returned from
        (PRAW) user.get_comments to the database. THis function must be
        called for each new comment API call. 'it' menas comment below.

        Keyword arguments:
        self -- instantiates object
        Ac -- Number of accounts active (at time of call)
        ScHd -- Min comment score to hide
        Cr -- When created
        CrUt -- UTC time it was created (comment.created_utc)
        Dn -- Full subreddit description
        DnHl -- Full description in html
        DsNm -- Display name
        HF - Has fetched (subreddit.has_fetched)
        HImg -- Subreddit header image url
        HdTl -- Subreddit header title
        Id -- Subreddit id
        JSON -- JSON dictionary (honestly not completely sure)
        Na -- Name
        NSFW -- over 18 (boolean)
        PuDn -- Public description of subreddit
        PbTr -- public traffic (boolean)
        ST -- submission types allowed
        SLL -- Submit link label
        STex -- Submit button text
        STexH -- Submit Button text in html
        STexL -- Submit Button text label
        SbTp -- Subreddit type (public vs private)
        Size -- Number of subscribers
        Tl -- Title
        URL -- Subreddit URL """
  
        cur = self.con.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')

            
        # NR = int(0 if NR is None else NR)
        cur.execute("""INSERT INTO Subreddits
            (accounts_active, comment_score_hide_mins, created, created_utc,
            description, description_html, display_name, has_fetched,
            header_img, header_title, id, json_dict, name, over18,
            public_description, public_traffic, submission_type, 
            submit_link_label, submit_text, submit_text_html,
            submit_text_label, subreddit_type, subscribers, title, url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (Ac, ScHd, Cr, CrUt,
                Dn, DnHl, DsNm, HF, HImg, HdTl, Id, JSON, Na, NSFW, PuDn, PbTr, ST,
                SLL, STex, STexH, STexL, SbTp, Size, Tl, URL)) 
        self.con.commit()

