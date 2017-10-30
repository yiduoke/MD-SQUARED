from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3, os

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

def makeTables():
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS credentials(username TEXT, password TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS blogs(username TEXT, blog_name TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS entries(username TEXT, entry TEXT);')

    db.commit()
    db.close()

makeTables()

def getUsernames():
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute("SELECT * FROM credentials;")

    bigList = c.fetchall()
    usernames = {}
    for smallList in bigList:
        usernames[smallList[0]] = smallList[1]

    return usernames
        
def addUser(username, password):
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    
    usernames = getUsernames()
    
    if (username in usernames):
        return 0 #username already exists
    else:
        c.execute('INSERT INTO credentials VALUES(?, ?);', [username, password])
        c.execute('select count(*) from credentials;')
        c.execute('INSERT INTO blogs VALUES(?, ?);', [username, "%s's Blog" %(username)])
        db.commit()
        db.close()
        return 1 #successful signup

def checkLogin(username, password):
    db = sqlite3.connect("databases.db")
    c = db.cursor()

    usernames = getUsernames()
    
    if (username in usernames):
        if (usernames[username] == password):
            return 0; #everything correct
        else:
            return 1; #wrong password
    else:
        return 2; #wrong username

def updateEntries(username, entry):
    db = sqlite3.connect("databases.db")
    c = db.cursor()

    c.execute('INSERT INTO entries VALUES (?, ?);', [username, entry])#shouldn't just be insert -- we have to enable updating too (I think)

    db.commit()
    db.close()

def editEntries(username, index, newEntry):
    db = sqlite3.connect("databases.db")
    c = db.cursor()

    newIndex=int(index)
    bigList=getEntries(username)
    oldEntry=bigList[newIndex]

    c.execute('UPDATE entries SET entry = "%s" WHERE entry = "%s" AND username = "%s";' %(newEntry,oldEntry,username))
    
    db.commit()
    db.close()

def getBlogs():
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute("SELECT * FROM blogs;")

    bigList = c.fetchall()
    blogs = {}
    for smallList in bigList:
        blogs[smallList[0]] = smallList[1]

    return blogs

def getEntries(username):
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute("SELECT * FROM entries WHERE username = ?;", [username])

    bigList = c.fetchall()
    entries = []
    for smallList in bigList:
        entries.append(smallList[1])

    return entries

#------------------------------------------------------------------------------------------------------------------------------------------

@my_app.route("/", methods = ['GET','POST'])
def root():
    if ("username" in session):
        return render_template('home.html', username = session["username"], loggedIn = True, blogs = getBlogs())
    else:
        return render_template('home.html', username = "guest", loggedIn=False, blogs = getBlogs())

@my_app.route("/login",methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

@my_app.route("/auth", methods = ["GET","POST"])
def auth():
    error = checkLogin(request.form["username"], request.form["password"])
    if (error == 0):# everything good
        session["login"] = True
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        flash("yay you're in!")
        return redirect(url_for('root'))
    elif (error == 1):#wrong password
        flash("wrong password")
        return redirect(url_for('root'))
    else:#wrong username
        flash("wrong username")
        return redirect(url_for('root'))

@my_app.route("/signup", methods = ['GET','POST'])
def signup():
    return render_template("newaccount.html")

@my_app.route("/signedUp", methods = ["GET","POST"])
def signedUp():
    error = addUser(request.form["username"], request.form["password"])
    if error == 0:
        flash("username already exists")
        return redirect(url_for("signup"))
    else:
        flash("signup successful")
        return redirect(url_for("login"))

@my_app.route("/search",methods = ['GET', 'POST'])
def search():
    pass

@my_app.route("/newEntry", methods = ['GET', 'POST'])
def newPost():
    updateEntries(session["username"], request.form["entry"])
    return redirect(url_for("blog", username = session["username"]))

@my_app.route("/editEntry<index>", methods = ['GET', 'POST'])
def editEntry(index):
    editEntries(session["username"], index, request.form["entry"])
    return redirect(url_for("blog", username = session["username"]))

@my_app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear() #removes all the session details
    return redirect(url_for("root"))

#Fix this so you can't just enter /something in url and get a page
@my_app.route("/<username>", methods = ['GET', 'POST'])
def blog(username):
    if ("username" in session and session["username"]==username):
        ownBlog1=True;
    else:
        ownBlog1=False;
    return render_template("blog_template.html", username = username, entries = getEntries(username),ownBlog=ownBlog1)

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
