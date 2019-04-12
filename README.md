## Live Data Plotting
Thanks to [Tom Diethe](https://github.com/tdiethe/flask-live-charts)

![](live-random-data.png?raw=true)

#### Technologies
```
  flask
  sse
  hightchart.js
  thread
  json
  jquery
```

#### Dependencies
```
  json
  flask
  queue
  thread
  gevent
```
#### Running

```
    
   ```
Follow the steps below to get a development env up and running in a ubuntu(linux).

1. Go to your main project folder.
```
$ cd <path-to-the-folder>
```
2. git clone the repository.
```
$ git clone git@github.com:cognitiveRobot/flask-sse-live-graph-demo.git
```
3. Go inside the cloned folder.
```
$ cd flask-sse-live-graph-demo
```
4. Create a Virtual Environment
```
$ python3 -m venv venv
```
5. Activate the Virtual Environment
```
$ souce venv/bin/activate
```
6. Upgrade the pip
```
$ pip install --upgrade pip
```
7. Install all python packages
```
$ pip install -r requirments.txt
```
8. If everything goes well up to now, then you would be able to quickly run the app.
```
$ python app.py
```

then go to http://127.0.0.1:5000/ 

```
