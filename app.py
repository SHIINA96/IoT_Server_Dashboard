# Setting sqlalchemy
from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
	
# Create engine
engine = create_engine("mysql+mysqlconnector://bob:secret@localhost:3306/Arduino")


# Web setting
from flask import Flask, render_template, Response
from queue import Queue
import threading
import gevent
import os, sys, time

app = Flask(__name__)
app.debug = True

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

@app.route('/')
def index():
	print("Index requested")
	return render_template('home.html')

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



if __name__ == "__main__":
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
			app.run()
		except:
			print ("Streaming stopped")
			os._exit(1)