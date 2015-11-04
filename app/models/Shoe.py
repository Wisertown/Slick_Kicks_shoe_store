from flask import Flask, render_template, redirect, url_for, session, request, flash
import re
import time
from time import mktime
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
from system.core.model import Model

class Shoe(Model):
    def __init__(self):
        super(Shoe, self).__init__()


    def add_shoe(self, shoe_details):
        insert_shoe_query = "INSERT into shoes (name, price, seller_id, buyer, created_at, updated_at) VALUES ('{}', '{}', '{}','{}', NOW(), NOW())".format(shoe_details['name'], shoe_details['price'], session['id'], 0) 
        return self.db.query_db(insert_shoe_query)

    def not_sold(self):
        not_sold_query = "SELECT id, name, price, created_at from shoes where seller_id = '{}' and buyer = 0".format(session['id'])
        print "Model not_sold"
        return self.db.query_db(not_sold_query)

    def shoe_sales(self):
        sale_query = "SELECT users.first_name, users.last_name, shoes.name, shoes.price, shoes.buyer, shoes.updated_at, shoes.seller_id from shoes join users on shoes.buyer = users.id where seller_id = '{}'".format(session['id'])
        return self.db.query_db(sale_query)

    def get_all_products(self):
        get_all_products_query = "SELECT concat(users.first_name, users.last_name)as full_name, concat(users.id)as id_user, concat(shoes.id)as id_shoe, concat(shoes.name)as shoe_name, shoes.price, shoes.created_at from users join shoes on users.id = shoes.seller_id where buyer = 0"
        return self.db.query_db(get_all_products_query)

    def buy(self, id):
        success = []
        print "Made it here to the model"
        buy_shoe_query = "UPDATE shoes set buyer = '{}' where shoes.id = '{}'".format(session['id'], id)
        return self.db.query_db(buy_shoe_query)
        print "made it here after the query"
        success.append("Congratulations! You just bought some SICK KICKS!")

    def get_purchases(self):
        purchase_query = "SELECT users.first_name, users.last_name, shoes.name, shoes.price, shoes.buyer, shoes.updated_at, shoes.seller_id from shoes join users on shoes.seller_id = users.id where buyer ='{}'".format(session['id'])
        return self.db.query_db(purchase_query)

    def delete(self, id):
        delete_query ="DELETE from shoes WHERE shoes.id = '{}'".format(id)
        return self.db.query_db(delete_query) 

        