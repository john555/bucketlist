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
        
    return render_template("login.html", error=True)

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

    bucket = app_manager.users[user_id]

    return render_template("dashboard.html", user=app_manager.users[user_id], bucket=bucket)

@app.route("/buckets/", methods=['POST'])
def get_buckets():
    if not request.method == 'POST':
        return redirect(url_for("page_not_found"))
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


@app.route('/buckets/<bucket_id>/add', methods = ['POST'])
def add_item_to_bucket(bucket_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = app_manager.users[user_id]
        
        if not bucket_id in user.buckets:
            return json.dumps(dict(error="Bucket was not found."))
        
        bucket = user.buckets[bucket_id]
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']   
        item = bucket.create_item(title, description, date)
        response = dict()
        response['title'] = item.title
        response['is_complete'] = item.is_complete
        response['description'] = item.description
        response['target_date'] = item.target_date
        response['timestamp'] = item.timestamp
        return json.dumps(response)

    return json.dumps(dict(error="Unauthorized request."))

@app.route('/buckets/<bucket_id>/edit', methods = ['POST'])
def edit_bucket(bucket_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = app_manager.users[user_id]
        name = request.form['name']
        user.edit_bucket(bucket_id, name)
        return json.dumps(dict(bucket_id=bucket_id, name=name))

@app.route('/buckets/<bucket_id>/delete', methods = ['POST'])
def delete_bucket(bucket_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = app_manager.users[user_id]
        user.delete_bucket(bucket_id)
        return json.dumps(dict(bucket_id = bucket_id))

@app.route("/buckets/<bucket_id>/complete/<item_id>", methods=['POST'])
def make_item_complete(bucket_id, item_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = app_manager.users[user_id]
        if bucket_id in user.buckets:
            bucket = user.buckets[bucket_id]
            bucket.set_complete(item_id)
            return json.dumps(dict(item_id=item_id))
        else:
            return json.dumps(dict(error="Unknown bucket"))

@app.route("/buckets/<bucket_id>/incomplete/<item_id>", methods=['POST'])
def make_item_incomplete(bucket_id, item_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = app_manager.users[user_id]

        if bucket_id in user.buckets:
            bucket = user.buckets[bucket_id]
            bucket.set_incomplete(item_id)
            return json.dumps(dict(item_id=item_id))
        else:
            return json.dumps(dict(error="Unknown bucket"))

@app.route("/buckets/<bucket_id>/delete/<item_id>", methods=['POST'])
def delete_item(bucket_id, item_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = app_manager.users[user_id]

        if bucket_id in user.buckets:
            bucket = user.buckets[bucket_id]
            bucket.delete_item(item_id)
            return json.dumps(dict(item_id=item_id))
        else:
            return json.dumps(dict(error="Unknown bucket"))

@app.route("/buckets/<bucket_id>/edit/<item_id>", methods=['POST'])
def edit_item(bucket_id, item_id):
    if 'user_id' in session:
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        user_id = session['user_id']
        user = app_manager.users[user_id]

        if bucket_id in user.buckets:
            bucket = user.buckets[bucket_id]
            bucket.edit_item(item_id, title, description, date)
            return json.dumps(dict(item_id=item_id))
        else:
            return json.dumps(dict(error="Unknown bucket"))
#
# Error handlers
#
@app.route('/pagenotfound')
def page_not_found():
    return render_template("404.html"), 404


# @app.errorhandler(405)
# def method_not_allowed():
#     return render_template("404.html"), 405

if __name__ == '__main__':
    app.secret_key = 'hkhfkj7937489234nd94329rb9n0m98'
    app.config['SESSION_TYPE'] = 'filesystem'

    #session.init_app(app)
    app.run(debug=True)
