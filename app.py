# Setting sqlalchemy
from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Create engine
engine = create_engine("mysql+mysqlconnector://bob:secret@localhost:3306/Arduino")

# Web setting
from flask import Flask, render_template, make_response, Response, request, redirect, url_for, logging, session, flash, jsonify
from queue import Queue
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_cors import CORS

# A Pythone Sheet
from devices import Devices

import json
import datetime
import requests
import threading
import gevent
import os, sys
import time


app = Flask(__name__)
CORS(app, supports_credentials=True)
devices = Devices()

qHumi = Queue()
qTemp = Queue()
qSoil = Queue()
qTempChart = Queue()
qHumiChart = Queue()

qTemperatureMedian = Queue()
qTemperatureMean = Queue()
qTemperatureMode = Queue()

qHumidityMedian = Queue()
qHumidityMean = Queue()
qHumidityMode = Queue()

############### Logger Definition Start ###############
# To do - Class for Logger and Publisher
# Logging temp data - simulation
# To do - Error handling.

temperature_value = 0
humidity_value = 0
soil_value = 0
def log_temp(name):
    # print("Starting " + name)
    gevent.sleep(5)
    while True:
        global temperature_value, humidity_value, soil_value
        
        # Pull data from database
        connection = engine.connect()
        temperature_value = connection.execute("select Temperature_Value from Temperature_Data order by Data_ID DESC LIMIT 1")
        for row in temperature_value:
            # print("Temperature:", row['Temperature_Value'])
            temp = row['Temperature_Value']
            global temperatureLiveValue
            temperatureLiveValue = temp
        connection.close()

        # Pull data from database
        connection = engine.connect()
        humidity_value = connection.execute("select Humidity_Value from Humidity_Data order by Data_ID DESC LIMIT 1")
        for row in humidity_value:
            # print("Humidity:", row['Humidity_Value'])
            humi = row['Humidity_Value']
            global humidityLiveValue
            humidityLiveValue = humi
        connection.close()

        # Pull data from database
        connection = engine.connect()
        soil_value = connection.execute("select Soil_State from Soil_Moisture_Data order by Data_ID DESC LIMIT 1")
        for row in soil_value:
            # print("Soil State:", row['Soil_State'])
            soil = row['Soil_State']
            global soilLiveValue
            soilLiveValue = soil
        connection.close()
        
        # print("temp added in the queue")
        qTemp.put(temp)
        qHumi.put(humi)
        qSoil.put(soil)
        gevent.sleep(0.5)        
     
temperatureChart_value = 0
humidityChart_value = 0
def log_tempChart(name):
    #print("Starting " + name)
    gevent.sleep(5)
    while True:
        global temperatureChart_value
        global humidityChart_value
        connection = engine.connect()
        temperatureChart_value = connection.execute("select Temperature_Value from Temperature_Data order by Data_ID DESC LIMIT 1")
        for row in temperatureChart_value:
            #print("Temperature:", row['Temperature_Value'])
            tempChart = row['Temperature_Value']
            global temperatureChartValue
            temperatureChartValue = tempChart
        connection.close()
        connection = engine.connect()
        humidityChart_value = connection.execute("select Humidity_Value from Humidity_Data order by Data_ID DESC LIMIT 1")
        for row in humidityChart_value:
            #print("Humidity:", row['Humidity_Value'])
            humiChart = row['Humidity_Value']
            global humidityChartValue
            humidityChartValue = humiChart
        connection.close()

        # print("temp added in the queue")
        qTempChart.put(tempChart)
        qHumiChart.put(humiChart)
        gevent.sleep(0.5)


temperatureMean_value = 0
temperatureMedian_value = 0
temperatureMode_value = 0
def log_tempAnalysis(name):
    gevent.sleep(5)
    while True:
        global temperatureMean_value, temperatureMedian_value, temperatureMode_value
        connection = engine.connect()
        temperatureMean_value = connection.execute("select Temperature_Mean from Temperature_Analysis_Mean where Temperature_Mean is not null order by Data_ID DESC limit 1")
        for row in temperatureMean_value:
            tempMean = row['Temperature_Mean']
            global temperatureMeanValue
            temperatureMeanValue = tempMean
        connection.close()

        connection = engine.connect()
        temperatureMedian_value = connection.execute("select Temperature_Median from Temperature_Analysis_Median where Temperature_Median is not null order by Data_ID DESC limit 1")
        for row in temperatureMedian_value:
            tempMedian = row['Temperature_Median']
            global temperatureMedianValue
            temperatureMedianValue = tempMedian
        connection.close()

        connection = engine.connect()
        temperatureMode_value = connection.execute("select Temperature_Mode from Temperature_Analysis_Mode where Temperature_Mode is not null order by Data_ID DESC limit 1")
        for row in temperatureMode_value:
            tempMode = row['Temperature_Mode']
            global temperatureModeValue
            temperatureModeValue = tempMode
        connection.close()

        qTemperatureMean.put(tempMean)
        qTemperatureMedian.put(tempMedian)
        qTemperatureMode.put(tempMode)
        gevent.sleep(0.5)

humidityMean_value = 0
humidityMedian_value = 0
humidityMode_value = 0
def log_humiAnalysis(name):
    gevent.sleep(5)
    while True:
        global humidityMean_value, humidityMedian_value, humidityMode_value
        connection = engine.connect()
        humidityMean_value = connection.execute("select Humidity_Mean from Humidity_Analysis_Mean where Humidity_Mean is not null order by Data_ID DESC limit 1")
        for row in humidityMean_value:
            humiMean = row['Humidity_Mean']
            global humidityMeanValue
            humidityMeanValue = humiMean
        connection.close()

        connection = engine.connect()
        humidityMedian_value = connection.execute("select Humidity_Median from Humidity_Analysis_Median where Humidity_Median is not null order by Data_ID DESC limit 1")
        for row in humidityMedian_value:
            humiMedian = row['Humidity_Median']
            global humidityMedianValue
            humidityMedianValue = humiMedian
        connection.close()

        connection = engine.connect()
        humidityMode_value = connection.execute("select Humidity_Mode from Humidity_Analysis_Mode where Humidity_Mode is not null order by Data_ID DESC limit 1")
        for row in humidityMode_value:
            humiMode = row['Humidity_Mode']
            global humidityModeValue
            humidityModeValue = humiMode
        connection.close()

        qHumidityMean.put(humiMean)
        qHumidityMedian.put(humiMedian)
        qHumidityMode.put(humiMode)
        gevent.sleep(0.5)

############### Logger Definition End ###############


############### Stream Definition Start ###############
# streaming logged data
def streamTemp_data():
    #print("Starting streaming")
    while True:
        if not qTemp.empty() and not qHumi.empty() and not qSoil.empty():
            resultLiveData = [temperatureLiveValue, humidityLiveValue, soilLiveValue]
            yield 'data: ' + json.dumps(resultLiveData) + "\n\n"
            gevent.sleep(.4)
        else:
            gevent.sleep(1) # Try again after 1 sec
            # os._exit(1)
            
def streamTemperatureChart_Data():
    #print("Starting streaming")
    while True:
        if not qTempChart.empty() and not qHumiChart.empty():
            resultTempChart = [(time.time())*1000, temperatureChartValue]
            yield 'data: ' + json.dumps(resultTempChart) + "\n\n"
            gevent.sleep(1)
        else:
            gevent.sleep(1) # Try again after 1 sec
            # os._exit(1)

def streamHumidityChart_Data():
    print("Starting streaming")
    while True:
        if not qTempChart.empty() and not qHumiChart.empty():
            resultHumiChart = [(time.time())*1000, humidityChartValue]
            yield 'data: ' + json.dumps(resultHumiChart) + "\n\n"
            gevent.sleep(1)
        else:
            gevent.sleep(1) # Try again after 1 sec
            # os._exit(1)

def streamTemperatureAnalysis_data():
    while True:
        if not qTemperatureMean.empty() and not qTemperatureMedian.empty() and not qTemperatureMode.empty():
            resultTemperatureAnalysis = [temperatureMeanValue, temperatureMedianValue, temperatureModeValue]
            yield 'data: ' + json.dumps(resultTemperatureAnalysis) + "\n\n"
            gevent.sleep(1)
        else:
            gevent.sleep(1)

def streamHumidityAnalysis_data():
    while True:
        if not qHumidityMean.empty() and not qHumidityMedian.empty() and not qHumidityMode.empty():
            resultHumidityAnalysis = [humidityMeanValue, humidityMedianValue, humidityModeValue]
            yield 'data: ' + json.dumps(resultHumidityAnalysis) + "\n\n"
            gevent.sleep(1)
        else:
            gevent.sleep(1)

def time_converter(time: int) -> str:
    """
    Convert time from server format (unix timestamp), to readable human format.
    :param time: server unix timestamp.
    :return: readable human time format.
    """
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

############### Stream Definition End ###############
  
          
############### Register Form Class Start ###############

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')
    
############### Register Form Class End ###############


############### Route Definition Start ###############

# Home page route
@app.route('/')
def home():
    
    #print("Index requested")
    return render_template('home.html')
    
# dashboard Route/Page
@app.route('/dashboard')
def dashboard():

    # For Current Temperature
    r1 = requests.get('http://api.openweathermap.org/data/2.5/weather?id=2193734&mode=json&units=metric&APPID=32e936bdd92d8f51716f169539355294')
    json_object1 = r1.json()
    sky = json_object1['weather'][0]['main']
    temp = json_object1['main']['temp']
    pressure = json_object1['main']['pressure']
    humidity = json_object1['main']['humidity']
    tempMax = json_object1['main']['temp_max']
    tempMin = json_object1['main']['temp_min']
    visibility = json_object1['visibility']
    windSpeed = json_object1['wind']['speed']
    windDegree = json_object1['wind']['deg']
    cloudiness = json_object1['clouds']['all']
    sunrise=time_converter(json_object1['sys']['sunrise'])
    sunset=time_converter(json_object1['sys']['sunset'])
    city=json_object1['name']
    country = json_object1['sys']['country']

    # For weather Forecast
    r2 = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Auckland,nz&mode=json&units=metric&APPID=32e936bdd92d8f51716f169539355294')
    json_object2 = r2.json()
    forecastTime1 = time_converter(json_object2['list'][2]['dt'])
    forecastWeather1 = json_object2['list'][2]['weather'][0]['description']
    forecastTemperature1 = json_object2['list'][2]['main']['temp']
    forecastHumidity1 = json_object2['list'][2]['main']['humidity']
    forecastPressure1 = json_object2['list'][2]['main']['pressure']
    forecastWindSpeed1 = json_object2['list'][2]['wind']['speed']
    forecastTime2 = time_converter(json_object2['list'][4]['dt'])
    forecastWeather2 = json_object2['list'][4]['weather'][0]['description']
    forecastTemperature2 = json_object2['list'][4]['main']['temp']
    forecastHumidity2 = json_object2['list'][4]['main']['humidity']
    forecastPressure2 = json_object2['list'][4]['main']['pressure']
    forecastWindSpeed2 = json_object2['list'][4]['wind']['speed']
    forecastTime3 = time_converter(json_object2['list'][6]['dt'])
    forecastWeather3 = json_object2['list'][6]['weather'][0]['description']
    forecastTemperature3 = json_object2['list'][6]['main']['temp']
    forecastHumidity3 = json_object2['list'][6]['main']['humidity']
    forecastPressure3 = json_object2['list'][6]['main']['pressure']
    forecastWindSpeed3 = json_object2['list'][6]['wind']['speed']
    forecastTime4 = time_converter(json_object2['list'][8]['dt'])
    forecastWeather4 = json_object2['list'][8]['weather'][0]['description']
    forecastTemperature4 = json_object2['list'][8]['main']['temp']
    forecastHumidity4 = json_object2['list'][8]['main']['humidity']
    forecastPressure4 = json_object2['list'][8]['main']['pressure']
    forecastWindSpeed4 = json_object2['list'][8]['wind']['speed']

    #print("Dashboard")
    return render_template('dashboard.html', devices=devices, sky=sky, temp=temp, pressure=pressure, humidity=humidity, tempMax=tempMax, tempMin=tempMin, visibility=visibility, windSpeed=windSpeed, windDegree=windDegree, cloudiness=cloudiness, sunrise=sunrise, sunset=sunset, city=city, country=country, forecastTime1=forecastTime1, forecastWeather1=forecastWeather1, forecastHumidity1=forecastHumidity1, forecastPressure1=forecastPressure1, forecastWindSpeed1=forecastWindSpeed1, forecastTime2=forecastTime2, forecastWeather2=forecastWeather2, forecastHumidity2=forecastHumidity2, forecastPressure2=forecastPressure2, forecastWindSpeed2=forecastWindSpeed2, forecastTime3=forecastTime3, forecastWeather3=forecastWeather3, forecastHumidity3=forecastHumidity3, forecastPressure3=forecastPressure3, forecastWindSpeed3=forecastWindSpeed3,  forecastTime4=forecastTime4, forecastWeather4=forecastWeather4, forecastTemperature1=forecastTemperature1, forecastTemperature2=forecastTemperature2, forecastTemperature3=forecastTemperature3, forecastTemperature4=forecastTemperature4, forecastHumidity4=forecastHumidity4, forecastPressure4=forecastPressure4, forecastWindSpeed4=forecastWindSpeed4)
    
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

# Temperature Data Upload Route
@app.route('/streamTemp/', methods=['GET', 'POST'])
def streamTemp():
    # gevent.sleep(1)
    #print("stream requested/posted")
    return Response(streamTemp_data(), mimetype="text/event-stream")
  
# Highcharts Route
@app.route('/streamTemperatureChart/', methods=['GET', 'POST'])
def streamTemperatureChart():
    # gevent.sleep(1)
    #print("stream requested/posted")
    return Response(streamTemperatureChart_Data(), mimetype="text/event-stream")

@app.route('/streamHumidityChart/', methods=['GET', 'POST'])
def streamHumidityChart():
    # gevent.sleep(1)
    #print("stream requested/posted")
    return Response(streamHumidityChart_Data(), mimetype="text/event-stream")


# Temperature Analysis Data Route
@app.route('/streamTemperatureAnalysis/', methods=['GET', 'POST'])
def streamTemperatureAnalysis():
    return Response(streamTemperatureAnalysis_data(), mimetype="text/event-stream")

# Humidity Analysis Data Route
@app.route('/streamHumidityAnalysis/', methods=['GET', 'POST'])
def streamHumidityAnalysis():
    return Response(streamHumidityAnalysis_data(), mimetype="text/event-stream")
    
# Device Control Route
@app.route('/devices', methods=['POST'])
@is_logged_in
def decives():
    if request.method == "POST":
        json = request.get_json()
        device = json["device"]
        status = json["status"]
        controlType = json['controlType']
        connection = engine.connect()
        connection.execute("INSERT INTO Actuator (Actuator_Name, Actuator_State, Control_Type) Values (%s,%s,%s)",(device, status, controlType))
        print(device)
        print(status)
        print(controlType)
    # else:
        return jsonify(device = device)
        
############### Route Definition End ###############


if __name__ == '__main__':
    try:
        thTemp = threading.Thread(target=log_temp, args=("temp_logger",))
        thTempChart = threading.Thread(target=log_tempChart, args=("tempChart_logger",))
        thTempAnalysis = threading.Thread(target=log_tempAnalysis, args=("tempAnalysis_logger",))
        thHumiAnalysis = threading.Thread(target=log_humiAnalysis, args=("humiAnalysis_logger",))
        
        thTemp.start()   
        thTempChart.start()
        thTempAnalysis.start()
        thHumiAnalysis.start()

        print ("Thread(s) started..")
    except:
        print ("Error: unable to start thread(s)")
        os._exit(1)
    else:
        # start streaming
        try:
            app.secret_key = 'verySecret#123'
            app.run(debug=True, threaded = True, host='127.0.0.1', port=5000)
            # app.run(debug=True, threaded = True, host='192.168.1.68', port=5000)

        except:
            print ("Streaming stopped")
            os._exit(1)
    