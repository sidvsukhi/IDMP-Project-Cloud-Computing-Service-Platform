from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__)


app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'cloudcomputingDB'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM authorization WHERE userName = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            #session['id'] = account['authID']
            session['username'] = account['userName']
            return redirect(url_for('profile'))
        else:
            msg = 'Incorrect username / password !'
            flash(msg,'error')
    return render_template('pages-login.html')
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    #session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'name' in request.form and 'contact' in request.form and 'paymentMethod' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        contact = request.form['contact']
        paymentMethod = request.form['paymentMethod']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM authorization WHERE userName = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        else:
            cursor.execute('CALL generateUserAccount(% s, % s, % s, % s, % s, % s)', (username, password, email, name, contact, paymentMethod))
            cursor.close()
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            session['loggedin'] = True
            #session['id'] = account['authID']
            session['username'] = username
            return redirect(url_for('profile'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('pages-register.html', msg = msg)

@app.route("/profile", methods =['GET', 'POST'])
def profile():
    if not session.get('username') is None:
        username = session.get('username')
        #user = users[username]
        return render_template("index.html", user=username)

if __name__ == "__main__":
    app.run(debug=True)