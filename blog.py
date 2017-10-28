from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import os

f = "databases.db"

db = sqlite3.connect(f)
c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS creds(username TEXT, pass TEXT);')
c.execute('CREATE TABLE IF NOT EXISTS blogs(username TEXT, blogname TEXT, id INTEGER);')
c.execute('CREATE TABLE IF NOT EXISTS entries(entry TEXT, id INTEGER);')

def addUser(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute("SELECT * FROM creds;")
    bigList = c.fetchall()
    dict = {}
    for smallLists in bigList:
        dict[smallLists[0]] = smallLists[1]

    if (username in dict):
        return 0 #username already exists
    else:
        c.execute('INSERT INTO creds VALUES(?, ?);', [username, password])
        c.execute('select count(*) from creds;')
        c.execute('INSERT INTO blogs VALUES(?, ?, ?);', [username, c.fetchall()[0][0]-1, "%s's Blog" %(username)])
        db.commit()
        db.close()
        return 1 #successful signup

def checkLogin(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute("SELECT * FROM creds;")
    bigList = c.fetchall()
    dict = {}
    for smallLists in bigList:
        dict[smallLists[0]] = smallLists[1]
    
    if (username in dict):
        if (dict[username] == password):
            return 0; #everything correct
        else:
            return 1; #wrong password
    else:
        return 2; #wrong username

    db.commit()
    db.close()

def updateEntries(id, entry):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('INSERT INTO entries VALUES (?, ?);'%(id, entry))#shouldn't just be insert -- we have to enable updating too (I think)

    db.commit()
    db.close()

def updateBlog(username, blogName, id):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('INSERT INTO blogs VALUES(?, ?, ?);' [user, name, id])
    
    db.commit()
    db.close()
#---------------------------------------------------------------------------------------------------------------------

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

@my_app.route("/", methods = ['GET','POST'])
def root():
    if ("username" in session):
        return render_template('home.html', username = session["username"], loggedIn = True)
    else:
        return render_template('home.html', username = "guest", loggedIn=False)

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

@my_app.route("/signedUp",methods = ["GET","POST"])
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

@my_app.route("/newpost", methods = ['GET', 'POST'])
def newPost():
    render_template('edit.html')

@my_app.route("/edit",methods=['GET', 'POST'])
def editPost():
    render_template('edit.html', origtitle ='fromdatabase', origcontent = 'fromdatabase')

@my_app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear() #removes all the session details
    return redirect(url_for("root"))

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()

#------------------------------------------------------------------------------------------------------------------

db.commit()
db.close()
