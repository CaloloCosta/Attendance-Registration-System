# Attendance-Registration-System
First project for Software Engineering 1


## Installation
__*Backend*__
```
cd backend
virtualenv development
development\Scripts\activate.bat
pip install -e .
```

## How to run

##### Run the following commands in ```backend``` directory
```Activate the development enviroment```
```
Windows: development\Scripts\activate.bat
Linux: development/bin/activate
```
##### Set the environment variables

Replace ```set``` with ```export``` on a Linux machine
```
set FLASK_APP=flaskr
set FLASK_ENV=development
```
##### Run the web server
```
flask init-db
flask run
```
 

