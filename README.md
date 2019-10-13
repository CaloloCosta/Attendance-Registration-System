# Attendance-Registration-System
First project for Software Engineering 1


## How to install?
<ol>
  <li>In the folder backend</li>
  <li>Create the virtualenv  and activate it: <code>python3 -m venv development<br> . development/bin/activate</code>
    <br>On Windows: <code>$ py -3 -m venv development<br> development\Scripts\activate.bat</code></li>
  <li> Install flaskr: <code>pip install -e .</code></li>
</ol>

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
 

