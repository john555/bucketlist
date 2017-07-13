"""application routes"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from bucketlist.appmanager import ApplicationManager
from bucketlist.models import *
import json

# delete session if it exists
# if 'user_id' in session:
#     del session['user_id']
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
    if not 'user_id' in session:
        return redirect(url_for("login"))

    user_id = session['user_id']
    if not user_id in app_manager.users:
        return redirect(url_for("login"))
    
    return render_template("dashboard.html", user=app_manager.users[user_id], bucket=dict())

@app.route("/buckets/")
def get_buckets():
    result = []
    user_id = session.get('user_id')
    if user_id:
        buckets = app_manager.users[user_id].buckets
        for k, bucket in buckets:
            result.append(dict(id=k, name=bucket.name))

    return json.dumps(result)

@app.route("/buckets/create", methods=['POST'])
def add_bucket():
    if 'user_id' in session:
        user_id = session['user_id']
        name = request.form['name']
        user = app_manager.users[user_id]
        bucket = user.create_bucket(name)

        return "{\"bucket_id\":\""+bucket.bucket_id+"\",\"name\":\""+bucket.name+"\"}"

    return "{error:\"Authentication is required.\"}"

@app.route("/buckets/<bucket_id>")
def show_bucket_item(bucket_id):
    if 'user_id' in session:
        user_id = session['user_id']

        if not user_id in app_manager.users:
            return redirect(url_for("login"))

        user = app_manager.users[user_id]

        if not bucket_id in user.buckets:
            return redirect(url_for("page_not_found"))

        bucket = user.buckets[bucket_id]

        return render_template("dashboard.html", user = user, bucket = bucket)
    else:
        return redirect(url_for("login"))

@app.route('/pagenotfound')
def page_not_found():
    return render_template("404.html")
if __name__ == '__main__':
    app.secret_key = 'hkhfkj7937489234nd94329rb9n0m98'
    app.config['SESSION_TYPE'] = 'filesystem'

    #session.init_app(app)
    app.run(debug=True)
