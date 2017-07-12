"""application routes"""
from flask import Flask, render_template, request, redirect, url_for, session
from bucketlist.applicationmanager import ApplicationManager
from bucketlist.models import *

app_manager = ApplicationManager()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = app_manager.find_user_by_email(email)

        if not user:
            # email does not exist
            return render_template("login.html", error=True)
        if user:
            if password == user.password:
                session['user_id'] = user.user_id
                return redirect(url_for("dashboard"))
        
    return "Unsupported method"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        app_manager.create_user(first_name, last_name, email, password)
        return redirect(url_for('index'))

    return "Unsupported method"

@app.route("/logout", methods=['POST'])
def logout():
    del session['user_id']
    return redirect(url_for("login"))

@app.route("/u")
@app.route("/u/")
def dashboard():
    print(str(session))
    if not 'user_id' in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.secret_key = 'hkhfkj7937489234nd94329rb9n0m948'
    app.config['SESSION_TYPE'] = 'filesystem'

    #session.init_app(app)
    app.run(debug=True)
