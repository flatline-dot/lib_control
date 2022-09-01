### Lib manage system
Service allows you to control the movement of books in library. There are roles such as Manager and Reader. Implemented system of fines.<br>


#### Run
 ````python
 git clone https://github.com/flatline-dot/lib_control
 docker-compose up -d
 ````
 
 #### Create admin
 ````
 docker-compose run python manage.py createsuperuser
 ````
 #### Service allow on http://localhost:8000/

<br>![view](https://user-images.githubusercontent.com/76453758/175833304-03a82510-8237-472a-869f-839943776cf9.jpg)
