from system.core.controller import *
import re
import time
from time import mktime
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')


class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')

    def index(self):
        return self.load_view('index.html')

    def register(self):
        user_details = request.form
        result = self.models['User'].register(user_details)
        if result['status']:
            for msg in result['success']:
                flash(msg)
            return redirect('/')
        
        else:
            for msg in result['errors']:
                flash(msg)
            return redirect('/') 
        
            
    def login(self):
        user_details = request.form

        login_status = self.models['User'].login(user_details)
        if login_status['status']==True:
            session['id']=login_status['user']['id']
            session['first_name']=login_status['user']['first_name']
            return redirect('/show')
        else:
            for msg in login_status['errors']:
                flash(msg)
            return redirect('/') 