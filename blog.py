#To Do:
# Update changes.txt and design doc
# Delete branches

from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3, os

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

#--------------------------------------------------------------------------------------------------------------------------------------------------
#Beginning of database functions

#Makes the 3 tables if this is the first time running the blog site
def makeTables():
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS credentials(username TEXT, password TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS blogs(username TEXT, blog_name TEXT);')
    c.execute('CREATE TABLE IF NOT EXISTS entries(username TEXT, entry TEXT);')

    db.commit()
    db.close()

#The function must be called for the tables to be made
makeTables()

#Returns a dictionary of username:password pairs
def getCredentials():
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute("SELECT * FROM credentials;")

    bigList = c.fetchall()
    credentials = {}
    for smallList in bigList:
        credentials[smallList[0]] = smallList[1]

    return credentials

#Adds an account to the credentials and blogs tables if that account doesn't already exist, returns True if it worked, False if username is taken
def addUser(username, password):
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    
    credentials = getCredentials()
    
    if (username in credentials):
        return False
    else:
        c.execute('INSERT INTO credentials VALUES(?, ?);', [username, password])
        c.execute('INSERT INTO blogs VALUES(?, ?);', [username, "%s's Blog"%(username)])
        db.commit()
        db.close()
        return True

#Adds a post to entries table
def addEntry(username, entry):
    db = sqlite3.connect("databases.db")
    c = db.cursor()

    c.execute('INSERT INTO entries VALUES (?, ?);', [username, entry])

    db.commit()
    db.close()

#Updates specified entry with new content
def editEntry(username, index, newEntry):
    db = sqlite3.connect("databases.db")
    c = db.cursor()

    newIndex=int(index)
    bigList=getEntries(username)
    oldEntry=bigList[newIndex]

    c.execute('UPDATE entries SET entry = "%s" WHERE entry = "%s" AND username = "%s";' %(newEntry,oldEntry,username))
    
    db.commit()
    db.close()

#Returns a dictionary of username:blog_name pairs
def getBlogs():
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute("SELECT * FROM blogs;")

    bigList = c.fetchall()
    blogs = {}
    for smallList in bigList:
        blogs[smallList[0]] = smallList[1]

    return blogs

#Returns a list of all blog posts by a given user
def getEntries(username):
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute("SELECT * FROM entries WHERE username = ?;", [username])

    bigList = c.fetchall()
    entries = []
    for smallList in bigList:
        entries.append(smallList[1])

    return entries

#Returns a list of sublists of usernames and blog entries that contain a given query
def getMatches(query):
    db = sqlite3.connect("databases.db")
    c = db.cursor()
    c.execute("SELECT * FROM entries;")

    bigList = c.fetchall()
    matches = []
    for smallList in bigList:
        if(smallList[1].find(query) != -1):
            matches.append(smallList)

    return matches

#End of database functions
#--------------------------------------------------------------------------------------------------------------------------------------------------
#Beginning of flask functions


@my_app.route("/", methods = ['GET','POST'])
def root():
    if ("username" in session):
        return render_template('home.html', username = session["username"], loggedIn = True, blogs = getBlogs())
    else:
        return render_template('home.html', username = "guest", loggedIn=False, blogs = getBlogs())


@my_app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template('login.html')


@my_app.route("/authorize", methods = ["GET","POST"])
def authorize():
    credentials = getCredentials()

    if(request.form["username"] in credentials):
        if(credentials[request.form["username"]] == request.form["password"]):
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            flash("Login successful")
            return redirect(url_for('root'))
        else:
            flash("wrong password")
            return redirect(url_for('login'))
    else:
        flash("wrong username")
        return redirect(url_for('login'))

    
@my_app.route("/signup", methods = ['GET','POST'])
def signup():
    return render_template("newaccount.html")


@my_app.route("/signedUp", methods = ["GET","POST"])
def signedUp():
    if(addUser(request.form["username"], request.form["password"])):
        flash("signup successful")
        return redirect(url_for("login"))
    else:
        flash("username already exists")
        return redirect(url_for("signup"))

    
@my_app.route("/newEntry", methods = ['GET', 'POST'])
def newPost():
    addEntry(session["username"], request.form["entry"])
    return redirect(url_for("blog", username = session["username"]))


@my_app.route("/editEntry<index>", methods = ['GET', 'POST'])
def edit(index):
    editEntry(session["username"], index, request.form["entry"])
    return redirect(url_for("blog", username = session["username"]))


@my_app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for("root"))


@my_app.route("/<username>", methods = ['GET', 'POST'])
def blog(username):
    if(username in getCredentials()):
        return render_template("blog_template.html", username = username, entries = getEntries(username), ownBlog = ("username" in session and session["username"] == username), loggedIn = session.has_key("username"))
    else:
        return redirect(url_for("error"))

    
@my_app.route("/search", methods = ['GET', 'POST'])
def searchpage():
    if(request.form.has_key("query")):
        if ("username" in session):
            return render_template('home.html', username = session["username"], loggedIn = True, blogs = getBlogs(), searchResults = getMatches(request.form["query"]))
        else:
            return render_template('home.html', username = "guest", loggedIn=False, blogs = getBlogs(), searchResults = getMatches(request.form["query"]))
    else:
        return redirect(url_for("error"))
    

    
@my_app.route("/error", methods = ["GET", "POST"])
def error():
    return render_template("error.html")


if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
