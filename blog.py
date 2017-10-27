from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os

f = "databases.db"

db = sqlite3.connect(f)
c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS creds(username TEXT, pass TEXT);')
c.execute('CREATE TABLE IF NOT EXISTS userblog(username TEXT, blogname TEXT, id INTEGER);')
c.execute('CREATE TABLE IF NOT EXISTS blog(entry TEXT, id INTEGER);')

def updateCreds(user, passw):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('INSERT INTO creds VALUES(?,?)', [user, passw])

    db.commit()
    db.close()

def checkLogin(user, passw):
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute("SELECT name, mark FROM peeps, courses WHERE peeps.id=courses.id;")
    bigList = c.fetchall()
    dict = {}
    for smallLists in bigList:
        dict[smallList[0]] = smallList[1]
    
    if (dict.has_key(user)):
        if (dict[user] == passw):
            return 0; #everything correct
        else:
            return 1; #wrong password
    else:
        return 2; #wrong username

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
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('INSERT INTO userblog VALUES(?,?,?)' [user, name, idEntry])
    
    db.commit()
    db.close()
#---------------------------------------------------------------------------------------------------------------------

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

@my_app.route("/", methods = ['GET','POST'])
def root():
    if (session.has_key("username")):
        return render_template('home.html', username = session["username"], loggedIn = True, blogcontent = "something from the datatable")
    else:
        return render_template('home.html')

@my_app.route("/login", methods = ['GET', 'POST'])
def login():
    if (checkLogin(request.form(["username"],request.form(["password"]))) == 0){# everything good
        session["login"] = True
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        return render_template('login.html')
    }
    elif (checkLogin(request.form(["username"],request.form(["password"]))) == 1){#wrong password

    }
    else{#wrong username

    }

@my_app.route("/signup", methods = ['GET','POST'])
def signup():
    return render_template("newaccount.html")

@my_app.route("/signedUp",methods = ["GET","POST"])
def signedUp():
    # the following line cause an error. idk why. but if you comment them out the page loads
    updateCreds(request.form["username"], request.form["password"])
    return render_template("home.html");

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
    session.clear()
    #removes all the session details
    return render_template('home.html', loggingOut = True)

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()

#------------------------------------------------------------------------------------------------------------------

db.commit()
db.close()