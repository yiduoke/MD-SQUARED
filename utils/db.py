import sqlite3

f= "databases.db"

db = sqlite3.connect(f)
c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS creds(username TEXT, pass TEXT);')
c.execute('CREATE TABLE IF NOT EXISTS userblog(username TEXT, blogname TEXT, id INTEGER);')
c.execute('CREATE TABLE IF NOT EXISTS blog(entry TEXT, id INTEGER);')

db.commit()
db.close()

def updateCreds(user, passw):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('INSERT INTO creds VALUES(?,?)', [user, passw])

    db.commit()
    db.close()

def checkLogin(user, passw):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('SELECT EXISTS(SELECT 1 FROM creds WHERE username==? AND pass==? LIMIT 1);', [user, passw])

    db.commit()
    db.close()

blogUpdater = 'UPDATE blog SET entry += %s WHERE id = %s'

def updateBlog(newEntry, idEntry):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute(blogUpdater % (newEntry, idEntry))

    db.commit()
    db.close()

def updateUserBlog(user, name, idEntry):
    c.execute('INSERT INTO userblog VALUES(?,?,?)' [user, name, idEntry])

db.commit()
db.close()