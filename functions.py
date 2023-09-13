# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
@app.route('/etmaids/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    #return redirect(url_for('home'))

 #http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/etmaids/profile/<username>', methods=['GET'])
def photo_display(username):
    # Check if the user is logged in
    if request.method == 'GET':
        if 'loggedin' in session:

        # We need all the account info for the user so we can display it on the profile page
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
            account = cursor.fetchone()
            #user = account['username'] 
        photo = os.path.join(app.config['UPLOAD_FOLDER'], username + '.jpg')
       # photo = url_for('static', filename='uploads/' + 'four.jpg')
    #return redirect(url_for('static', filename='uploads/' + 'seven.jpg'))
    return redirect('profile.html', account=account, username=photo)
"""@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:

        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
   # return render_template('profile.html', photo=uploads)
"""