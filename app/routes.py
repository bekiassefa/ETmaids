from flask import render_template
from app import app

# Define your routes and views here
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/maids')
def Maids():
    return render_template('Maids.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def Login():
    return render_template('Login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')
