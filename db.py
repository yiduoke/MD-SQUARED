import sqlite3

f= "databases.db"

db = sqlite3.connect(f)
c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS creds(username TEXT, pass TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS userblog(username TEXT, blogname TEXT, id INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS ;blog(entry TEXT, id INTEGER)')

def updateCreds(user, passw):
    c.execute('INSERT INTO creds VALUES(?,?)', [user, passw])

blogUpdater = 'UPDATE blog SET entry += %s WHERE id = %s'

def updateBlog(newEntry, idEntry):
    c.execute(blogUpdater % (newEntry, idEntry))

def updateUserBlog(user, name, idEntry):
    c.execute('INSERT INTO userblog VALUES(?,?,?)' [user, name, idEntry])

db.commit()
db.close()
