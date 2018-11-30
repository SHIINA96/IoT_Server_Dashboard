from flask import Flask, render_template, request, redirect, url_for, logging, session, flash
from flask_sockets import Sockets
from wtforms import Form, StringField, PasswordField, validators
from flask_mysqldb import MySQL
from functools import wraps
from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import gevent.monkey
gevent.monkey.patch_all()
import gevent
import datetime
import threading
import json

from database import dbusers

app = Flask(__name__)
app.debug = True
sockets = Sockets(app)

db_users = dbusers() # Hiding database info from others

# Config MySQL
app.config['MYSQL_HOST'] = db_users['host']
app.config['MYSQL_USER'] = db_users['user']
app.config['MYSQL_PASSWORD'] = db_users['password']
app.config['MYSQL_DB'] = db_users['db']
app.config['MYSQL_CURSORCLASS'] = db_users['cursor']
mysql = MySQL(app)

# Logging temp data
def log_temp(name):
    print("Starting " + name)
    while True:
        global temp_c
        
        # Get From Fields
        temp_c = request.form['Temperature_Value']
        
        # Create cursor
        cur = mysql.connection.cursor()
        
        gevent.sleep(1)
        
        # Execute SQL
        temp_c = cur.execute('SELECT Temperature_Value FROM Temperature_data ORDER BY Data_ID DESC LIMIT 1;',[Temperature_data])
        ##temp_c = temp_c + 1000 # real sensor reading will go here.
        print("Temp " + str(temp_c))

humidity_c = 0
# Logging humidity data.  
def log_humidity(name):
    print("Starting " + name)
    while True:
        global humidity_c
        gevent.sleep(1)
        humidity_c = humidity_c + 1 # real sensor reading will go here.
        print("Humidity " + str(humidity_c))



@sockets.route('/time')
def time_socket(ws):
    """ Handler for websocket connections that constantly pushes
        the latest data.
    """
    while True:
        global humidity_c, temp_c
        gevent.sleep(1)
        data = json.dumps({'temp': temp_c, 'humidity': humidity_c, 'time': datetime.datetime.now().isoformat()})
        ws.send(data)



@app.route('/')
def hello():
    """ Render our default template
    """
    return render_template('home.html')

if __name__ == "__main__":
    # Create two threads as follows
    try:
       th1 = threading.Thread(target=log_temp, args=("temp_logger",))
       th2 = threading.Thread(target=log_humidity, args=("humidity_logger",))
       th1.start()
       th2.start()
       print ("Thread(s) started..")
    except:
        print ("Error: unable to start thread")
    else:
        server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
        server.serve_forever()
