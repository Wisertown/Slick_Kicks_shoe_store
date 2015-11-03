from flask import Flask, render_template, redirect, url_for, session, request, flash
import re
import time
from time import mktime
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
from system.core.model import Model

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def register(self, user_details):
        success = []
        errors = []
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

        if not user_details['first_name']:
            errors.append('first name cannot be blank')
        elif len(user_details['first_name']) < 2:
            errors.append("first name cannot be fewer than 2 letters!")
        
        if not user_details['last_name']:
            errors.append('last name cannot be blank')
        elif len(user_details['last_name']) < 2:
            errors.append("last cannot be fewer than 2 letters!")
        
        if not user_details['email']:
            errors.append('email cannot be blank')
        elif not EMAIL_REGEX.match(user_details['email']):
            errors.append("Invalid email address!, please use lower case when typing your email address")
        elif len(user_details['email']) < 2:
            errors.append("email cannot be fewer than 2 letters!")
        
        if not user_details['password']:
            errors.append('password cannot be blank')
        elif len(user_details['password']) < 5:
            errors.append("password cannot be fewer than 5 letters!")

        if not user_details['pw_confirm']:
            errors.append('password confirm cannot be blank')
        elif len(user_details['pw_confirm']) < 5:
            errors.append("password confirm cannot be fewer than 2 letters!")
        elif user_details['password'] != user_details['pw_confirm']:
            errors.append("passwords do not match") 

        if errors:
            return {'status': False, 'errors':
            errors}
            return redirect('/')

        else:
            
            success.append("Congratulations! Account created, please log in.")    
            password = user_details['password']
            passwordhash = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) Values ('{}', '{}', '{}', '{}', NOW(), NOW())".format(user_details['first_name'], user_details['last_name'], user_details['email'], passwordhash)
            self.db.query_db(query)
            return {'status': True, 'success': success}

    def login(self, user_details):
        errors = []
        if len(user_details['email']) < 2:
            errors.append("Email cannot be empty or fewer than 2 characters!")
        if not EMAIL_REGEX.match(user_details['email']):
            errors.append("Invalid email address!")
        if len(user_details['password']) < 2:
            errors.append("password cannot be less than 2 characters!")
        if not user_details['password']:
            errors.append('password cannot be blank')
        if errors:
            return {'status': False, 'errors': errors} 
            return redirect('/')

        password = user_details['password']
        query = "SELECT * FROM users WHERE EMAIL= '{}'".format(user_details['email'])
        user = self.db.query_db(query)
        if user and self.bcrypt.check_password_hash(user[0]['password'], password):       
            return {'status': True, 'user': user[0]}

