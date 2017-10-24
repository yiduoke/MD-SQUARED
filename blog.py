from flask import Flask, render_template, request, session, redirect, url_for
import os

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)


@my_app.route("/", methods = ['GET','POST'])
def root():
    session["login"] = True
    session["username"] = request.form["username"]
    session["password"] = request.form["password"]
    return render_template ('home.html', username = session["username"]) 
    


@my_app.route("/search",methods = ['GET', 'POST'])
def search():
    pass

@my_app.route("/newpost",methods=['POST'])
def newPost():
    pass

@my_app.route("/editpost",methods=['GET', 'POST'])
def editPost():
    pass

@my_app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear()
    #removes all the session details
    return redirect(url_for('root'))

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()

