import SQLOps

sql = SQLOps.SQLClass()

strt = 0
end = 2

userlist = sql.get_usernames(strt,end)
usersubs = dict()
for user in userlist:
    usersubs[user] = sql.get_usersubs(user)

print usersubs[userlist[0]]

    
