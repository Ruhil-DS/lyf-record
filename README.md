# lyf-record : MAD2 Project

Name: Pushpak Ruhil

Roll no.: 201F2001180

This is my submission for the final project for the course Modern Application Development II

Term 2(May term), 2022




# Project setup

--------------

## How to use

Before we could use the web app, we need to setup the environment and servers for it.

1) <b>Setting up the Flask server :</b>

   
   - From the QuantifiedSelfApp-FLASK folder, simply run the command 
    
             python3 main.py
  


2) <b> Setting up Redis server : </b>
    
    - in a new terminal tab, start the redis server by typing 
    ----
          redis-server


3) <b> Setting up mailhog : </b>
    
    - in a new terminal tab, start the Mail-Hog server by typing 
    ----             
           mailhog
    
4) <b> Setting up Celery Worker and Celery Beat : </b>

   In the QuantifiedSelfApp-FLASK of the project ->
    
    - in a new terminal tab, start the Celery Workers by typing 
    ----
          Celery --app main.celery_inst worker --loglevel=info
    
    ---- 
          Celery --app main.celery_inst beat --loglevel=info
   
5) <b> Setting up Vue CLI server(frontend) : </b>
    
   In the root folder of the project ->

    ---- 
          npm run serve


------------------
# Using the App
To use the app, we need to go to the front end server's URL

By Default, it would be ```http://localhost:8080/``` 

## Test user
```python
username = 'Pushpak'  # Case in-sensitive
password = 'abcd'  # All lower case
```

_**NOTE THAT**_ : _When you sign up with a new user, you will have to use a strong password, 
without which you wont be able to register. This test user has a simple password defined directly in the backend_


------------------
# Lyf Record
- In this project, I have made a v2 of my QuantifiedSelfApp that I built in the last term. 

### Additional features in v2:
 - VueJS frontend framework. Single Page Application.
 - Use of APIs
 - Use of Async backend jobs using Celery
 - Use of NoSQL server(Redis) for Caching, async jobs.
 - Daily E-mail reminders and monthly user reports as pdf in the mail.
