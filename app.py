# Setting sqlalchemy
from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Create engine
engine = create_engine("mysql+mysqlconnector://bob:secret@localhost:3306/Arduino")

# Web setting
from flask import Flask, render_template, request, redirect, url_for, logging, session, flash
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from queue import Queue
import threading
import gevent
import os, sys, time

#from database import dbusers
#from devices import Devices

app = Flask(__name__)
app.debug=True

#devices = Devices()

qHumi = Queue()
qTemp = Queue()


# To do - Class for Logger and Publisher

# Logging temp data - simulation
# To do - Error handling.
temperature_value = 0
def log_temp(name):
    print("Starting " + name)
    gevent.sleep(5)
    while True:
        global temperature_value
        
        # Pull data from database
        connection = engine.connect()
        temperature_value = connection.execute("select Temperature_Value from Temperature_Data order by Data_ID DESC LIMIT 1")
        for row in temperature_value:
            print("Temperature:", row['Temperature_Value'])
            temp = row['Temperature_Value']
        connection.close()
        
        # print("temp added in the queue")
        qTemp.put(temp)
        gevent.sleep(0.5)


# Logging humidity data - simulation
# To do - Error handling.
humidity_value = 0
def log_humidity(name):
    print("Starting " + name)
    gevent.sleep(5)
    while True:
        global humidity_value
        
        # Pull data from database
        connection = engine.connect()
        humidity_value = connection.execute("select Humidity_Value from Humidity_Data order by Data_ID DESC LIMIT 1")
        for row in humidity_value:
            print("Humidity:", row['Humidity_Value'])
            humi = row['Humidity_Value']
        connection.close()

        # print("humidity added in the queue")		
        qHumi.put(humi)
        gevent.sleep(0.5)

# streaming logged data
def streamTemp_data():
    print("Starting streaming")
    while True:
        if not qTemp.empty():
            resultTemp = qTemp.get()
            print("sent data: ", resultTemp)
            # print(result)
            yield 'data: %s\n\n' % str(resultTemp)
            gevent.sleep(.4)
        else:
            print ("QUEUE empty!! Unable to stream @",time.ctime())
            gevent.sleep(1) # Try again after 1 sec
            # os._exit(1)
            
# streaming logged data
def streamHumi_data():
    print("Starting streaming")
    while True:
        if not qHumi.empty():
            resultHumi = qHumi.get()
            print("sent data: ", resultHumi)
            # print(result)
            yield 'data: %s\n\n' % str(resultHumi)
            gevent.sleep(.4)
        else:
            print ("QUEUE empty!! Unable to stream @",time.ctime())
            gevent.sleep(1) # Try again after 1 sec
            # os._exit(1)
            
@app.route('/streamTemp/', methods=['GET', 'POST'])
def streamTemp():
    # gevent.sleep(1)
    print("stream requested/posted")
    return Response(streamTemp_data(), mimetype="text/event-stream")
    
@app.route('/streamHumi/', methods=['GET', 'POST'])
def streamHumi():
    # gevent.sleep(1)
    print("stream requested/posted")
    return Response(streamHumi_data(), mimetype="text/event-stream")
            
            
# Home route
@app.route('/')
def home():
    return render_template('home.html')

# About Route/Page
@app.route('/about')
def about():
    return render_template('about.html')

#Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')


# db = AppDatabase(app)
# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        connection = engine.connect()
        connection.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        connection.close()


        flash('Successful. You are registered. You may login.', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Start Connection with Database
        connection = engine.connect()

        # Execute SQL
        username_result = connection.execute('SELECT * FROM users WHERE username= %s', [username])
        for row in username_result:
            result = row['username']
        # To Tell the User is exest or not
        if result != []:
            # Get stored hash
            password_result = connection.execute('SELECT password FROM users WHERE username= %s', [username])
            for row in password_result:
                password = row['password']
            # Close Connection
            connection.close()

            # Compare Password
            if sha256_crypt.verify(password_candidate, password):
                #Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are logged in.', 'success')

                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user looged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized! Please login.', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout Route
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You successfully logged out', 'success')
    return redirect(url_for('login'))

# Dashboard Route
@app.route('/dashboard')
@is_logged_in
def dashboard():
    print("Dashboard")
    # Retriving data from database will go here
    # First will have to get the data from the database and then send to the view
    return render_template('dashboard.html')

# Device Control Route
@app.route('/device/<string:id>/<string:action>/')
@is_logged_in
def device_control(id, action):
    for index in range(len(devices)):
        if devices[index]['id'] == int(id):
            # Update status
            devices[index]['status'] = action
            # Turn on/off the device
            #Change the pin
            print(devices[index]['pin'])
            flash('Successful!! ' + devices[index]['name'] + ' updated', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    try:
        thTemp = threading.Thread(target=log_temp, args=("temp_logger",))
        thHumi = threading.Thread(target=log_humidity, args=("humidity_logger",))
        thTemp.start()
        thHumi.start()
        print ("Thread(s) started..")
    except:
        print ("Error: unable to start thread(s)")
        os._exit(1)
    else:
            # start streaming
        try:
            app.secret_key = 'verySecret#123'
            app.run()
        except:
            print ("Streaming stopped")
            os._exit(1)
