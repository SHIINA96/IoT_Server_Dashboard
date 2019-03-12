# iot-flask-template

A simple and lightwight template to build an Internet of Things (IoT) application using Flask and MySQL. It also can be used to build a live RESTful API to deploy on raspberry pi.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python
Virtual Environment
MySQL
Your IDE
```
### Resources
Check the followings to learn basic concepts about:
* Flask - [webpage](http://www.ntu.edu.sg/home/ehchua/programming/webprogramming/Python3_Flask.html#zz-4.)
* Materialize - [video](https://www.youtube.com/watch?v=gCZ3y6mQpW0&list=PL4cUxeGkcC9gGrbtvASEZSlFEYBnPkmff)


### Installing

The final file structure for the .
```
iot-flask-template
├── app.py
├── database.py
├── devices.py
├── README.md
├── requirments.txt
├── templates
│   ├── about.html
│   ├── dashboard.html
│   ├── home.html
│   ├── includes
│   │   ├── _formhelpers.html
│   │   ├── _messages.html
│   │   └── _navbar.html
│   ├── layout.html
│   ├── login.html
│   └── register.html
```
Follow the steps below to get a development env up and running in a ubuntu(linux).

1. Go to your main project folder.
```
$ cd <path-to-the-folder>
```
2. git clone the repository.
```
$ git clone git@github.com:cognitiveRobot/iot-flask-template.git
```
3. Go inside the cloned folder.
```
$ cd iot-flask-template
```
4. Create a Virtual Environment
```
$ python3 -m venv v-iot
```
5. Activate the Virtual Environment
```
$ souce v-iot/bin/activate
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
If all good so far, then follow next to know how to integrate the database for this app. If not, they raise an issue, I will reply asap.

## Intregating the MySQL Database

Considering you have installed MySQL in your system. Follow the steps below to integrate a MySQL database to store user details.

1. Create a table named users in your database as follows.

  ```
mysql> describe users;
+---------------+--------------+------+-----+-------------------+----------------+
| Field         | Type         | Null | Key | Default           | Extra          |
+---------------+--------------+------+-----+-------------------+----------------+
| id            | int(11)      | NO   | PRI | NULL              | auto_increment |
| name          | varchar(100) | YES  |     | NULL              |                |
| email         | varchar(100) | YES  |     | NULL              |                |
| username      | varchar(30)  | YES  |     | NULL              |                |
| password      | varchar(100) | YES  |     | NULL              |                |
| register_date | timestamp    | NO   |     | CURRENT_TIMESTAMP |                |
+---------------+--------------+------+-----+-------------------+----------------+
  ```
2. Create database.py file in the project root director (i.e. app.py and database.py will sit in the same folder) and save the following content.
```
def dbusers():
    db_users = {
            'id':1,
            'user':'<ur_mysql_username>',
            'password':'<ur_username's_password>',
            'db':'<your_database>',
            'host':'localhost',
            'cursor':'DictCursor'
    }
    return db_users
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```
## Deployment

Comming soon.

## Built With

* [Python](https://www.python.org/) - For Server Side Program
* [Flask](http://flask.pocoo.org/) - For Webapp Framework
* [MySQL](https://www.mysql.com/) - For Database
* [Materialize](https://materializecss.com) - For Front End

## Contributing

Make the pull request.

## Versioning

For now please [See the tags](https://github.com/cognitiveRobot/iot-flask-template/commits/master)

## Authors

* **Zulfikar Hossain** - *Initial work* - [CognitiveRobot](https://github.com/CognitiveRobot)
* **Maybe you**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Brad Traversy](https://github.com/bradtraversy/) - For the initial code.
* [Billie Thompson](https://gist.github.com/PurpleBooth) - For the this readme file template.
