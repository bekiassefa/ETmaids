from app import app
from flask import render_template, flash, request, redirect, url_for, session, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField  
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
import os


app.secret_key = 'loginto'
ImageDir = os.path.dirname(os.path.abspath(__file__))
mysql = MySQL(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Define your routes and views here
@app.route('/etmaids/')
def index():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        msg = session['First_Name']
        return render_template('index.html', msg=msg)
    # User is not loggedin redirect to login page
    #return redirect(url_for('login'))
    #return render_template('index.html')
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

@app.route('/etmaids/Login', methods=['GET', 'POST'])
def Login():
     # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['First_Name'] = account['First_Name']
            # Redirect to home page
            msg = 'hey' + account['First_Name'] + 'You are Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('Login.html', msg=msg)

@app.route('/etmaids/Register', methods=['GET', 'POST'])
def registration():
    phone_regex = '^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form:
        # Create variables for easy access
        fname = request.form['fname']
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
            cursor.execute('INSERT INTO accounts (password, email, First_Name, Last_Name, phone) VALUES (%s, %s, %s, %s, %s)', (password, email, fname, lname, phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('registration.html', msg=msg)

@app.route('/etmaids/profile_register', methods=['GET', 'POST'])
def profile_register():
    msg =''
    if request.method == 'POST' and 'username' in request.form and 'age' in request.form and 'religion' in request.form and 'residence' in request.form and 'experience' in request.form and 'salary' in request.form:
     username = request.form['username']
     age = request.form['age']
     religion = request.form['religion']
     residence = request.form['residence']
     salary = request.form['salary']
     experience = request.form['experience']
     if 'loggedin' in session:
      usr = session['id']
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      query = "UPDATE accounts SET username=%s, age=%s, salary=%s, experience=%s, residence=%s, religion=%s WHERE id=%s"
      val = (username, age, salary, experience, residence, religion, usr)
      cursor.execute(query, val)
      mysql.connection.commit()
      msg = 'profile updated successfully'
      return redirect(url_for('home', msg=msg))
    else:
        return  render_template('profile_form.html')


@app.route('/etmaids/home')
def home():
    if 'loggedin' in session:
      usr = session['First_Name']
    return render_template('home.html', usr=usr)



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)