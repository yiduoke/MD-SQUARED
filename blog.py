from flask import Flask, render_template, request, session, redirect, url_for
import os

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)


@my_app.route("/", methods = ['GET','POST'])
def root():
    # if (session.has_key["username"]):
    #     session["login"] = True
    #     session["username"] = request.form["username"]
    #     session["password"] = request.form["password"]
    #     return render_template ('home.html', username = session["username"], loggedIn = True, blogcontent = "something from the datatable")
    # else:
    return render_template ('home.html')

@my_app.route("/login", methods = ['GET', 'POST'])
def login():
    pass
    
    

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

