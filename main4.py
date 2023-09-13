from flask import Flask, flash, render_template, request, redirect, url_for, session, send_file, send_from_directory
from app import app
from flask import current_app
import urllib.request
from main1 import upload_image
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField  
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import os
#app = Flask(__name__)
ImageDir = os.path.dirname(os.path.abspath(__file__))
# Change this to your secret key (it can be anything, it's for extra protection)

# Intialize MySQL
mysql = MySQL(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/etmaids/')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    #return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/etmaids', methods=['GET', 'POST'])
def index():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            msg = username + 'Logged in successfully!'
            return render_template('home.html', username=session['username'])
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


    # http://localhost:5000/python/logout - this will be the logout page
@app.route('/etmaids/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/etmaids/register', methods=['GET', 'POST'])
def register():
    phone_regex = '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form:
        # Create variables for easy access
        fname = request.form['fsername']
        lname = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE phone = %s', (phone,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(phone_regex, phone):
            msg = 'invalid phone number!'
        elif not fname or not lname or not password or not email:
            msg = 'Please fill out the form!'
        #elif photo and allowed_file(photo.filename):
	     #   filename = secure_filename(photo.filename)
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
           # filename = secure_filename(photo.filename)
            #photo.save(os.path.join(app.config['UPLOAD_FOLDER'], username + '.jpg'))
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (fname, lname, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('registration.html', msg=msg)

@app.route('/etmaids/reg_detail')
def profile_register():
    if request.method == 'POST' and 'username' in request.form and 'age' in request.form and 'residence' in request.form and 'salary' in request.form and 'experience' in request.form and 'religion' in request.form:
     username = request.form['username']
     age = request.form['age']
     residence = request.form['residence']
     salary = request.form['salary']
     experience = request.form['experience']
     religion = request.form['religion']

     if 'loggedin' in session:

        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        id = account['id']
        Update_query = "UPDATE accounts SET username = %s, age = %s, residence = %s, religion =  %s, salary = %s, experience = %s, WHERE id = %s" 
        val = (username, age, residence, salary, experience, religion, id)
        cursor.excute(Update_query, val)
        msg = 'Successfuly Updated!'
    return render_template('profile_form.html', msg=msg)

@app.route('/etmaids/profile_display')
def profile_display():
    if 'loggedin' in session:

        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        id = account['id']
        return render_template('profile.html', account=account)
    return redirect(url_for('home'))

