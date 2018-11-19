from flask import Flask, render_template, json, request, redirect, url_for

import datetime

app = Flask(__name__)

userID = 'none'
password = 'none'

@app.route('/about',  methods=['GET', 'POST'])
def about():

    return render_template('about.html')

@app.route("/")
def main():

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            userID = request.form['username']
            password = request.form['password']
            return redirect(url_for('about'))
    return render_template('login.html', error=error)

@app.route('/level1ABC', methods=['GET', 'POST'])
def level1ABC():
    if userID != 'none' :

        return render_template('*****.html')
    else:
       return render_template('login.html') 

@app.route('/home',  methods=['GET', 'POST'])
def home():

    return render_template('index.html')


if __name__ == "__main__":
    app.run()