from flask import Flask, render_template, request
import db

app = Flask(__name__)
db.setup()

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name, messages=db.get_guestbook())

@app.post("/submit")
def submit():
    name = request.form.get("name")
    message = request.form.get("message")
    db.add_content(name, message)
    return render_template("hello.html", name=None, messages=db.get_guestbook())
