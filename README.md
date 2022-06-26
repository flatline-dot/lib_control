### Book managment system
Service allows you to control the movement of books in library. There are roles such as Manager and Reader. Implemented system of fines.<br>


#### Installation on Windows
 ````python
 git clone https://github.com/flatline-dot/lib_control
 python -m venv env
 env\Scripts\activate
 pip install -r requirements.txt
 ````
#### Run
 ````python
 python manage.py runsever
 ````
 #### Installation on Linux
  ````python
 git clone https://github.com/flatline-dot/lib_control
 sudo apt-get install python3-pip
 pip install redis
 python3 -m venv env
 source env/bin/activate
 pip install -r requirements.txt
 ````
#### Run with system of fines
 ````python
 sudo service redis-server start
 python3 manage.py runsever
 celery -A lib_control beat -l INFO
 celery -A lib_control worker -l INFO
 ````
