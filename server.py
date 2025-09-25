from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.post("/submit")
def submit():
    name = request.form.get("name")
    text = request.form.get("text")