from flask import Flask, render_template, request, session, redirect, url_for
import os

my_app = Flask(__name__)
my_app.secret_key = os.urandom(32)

login = {"hello":"life"}

@my_app.route("/", methods = ['GET','POST'])
def root():
    print session
    if "login" in session:
        return redirect(url_for('response'))
    else:
        return render_template('login.html', loggingOut = False, error = False, errorStatement = "")

@my_app.route("/response", methods = ['GET','POST'])
def response():
    for username in login:
        if (request.form["username"] == username):
            if(request.form["password"] == login[username]):
                session["login"] = True
                session["username"] = request.form["username"]
                session["password"] = request.form["password"]
                return render_template('welcome.html', username = session["username"]) 
            else:
                return render_template('login.html', loggingOut = False, error = True, errorStatement = "Invalid password.")
        else:
            return render_template('login.html', loggingOut = False, error = True, errorStatement = "Invalid username.")

        
@my_app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.clear()
    #removes all the session details
    return redirect(url_for('root'))
    #return render_template('form.html', loggingOut = True, error = False, errorStatement = "")

if __name__ == '__main__':
    my_app.debug = True
    my_app.run()

