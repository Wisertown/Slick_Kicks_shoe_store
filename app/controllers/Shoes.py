
from system.core.controller import * 
import re
import time
from time import mktime
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
from system.core.controller import *

class Shoes(Controller):
    def __init__(self, action):
        super(Shoes, self).__init__(action)
       
        self.load_model('Shoe')

    
    def index(self):
        """ 
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_all_users()
        """
        return self.load_view('dashboard.html')

    def create(self):
    	shoe_details = request.form
    	self.models['Shoe'].add_shoe(shoe_details)
    	return redirect('/show')

    def show(self):
    	shoe_data_query = self.models['Shoe'].not_sold()
        sales = self.models['Shoe'].shoe_sales()
        return self.load_view('dashboard.html', shoe_data_query=shoe_data_query, sales=sales)

    def logout(self):
    	session.clear()
    	return redirect('/')

    def all_products(self):
        get_all_products = self.models['Shoe'].get_all_products()
        return self.load_view('allshoes.html', show_shoes=get_all_products)
    
    def buy(self, id):
        result = self.models['Shoe'].buy(id)
        print id
        print "got here"
        flash('Congrats you bought this item!')
        return redirect('/all_products')


    # # def delete(self, id):
    #   shoe_delete_query = self.models['Shoe'].delete(id)
    #   return redirect('/show')


    # def show2(self):
    #   shoe_data_query = self.models['Shoe'].not_sold()
    #   return self.load_view('dashboard.html', shoe_data_query=shoe_data_query)



