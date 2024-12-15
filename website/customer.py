from flask import Blueprint, render_template, redirect, flash, url_for, request
import json
from moloni import *

customer = Blueprint('customer', __name__)

@customer.route('/', methods=['GET','POST'])
def menu():
    with open("tokens_moloni.json", "r") as tokens_moloni_file:
        token_dict = json.load(tokens_moloni_file)
    email = request.args.get('c')
    customer_data = get_customer_by_email(token_dict, email).json()
    name = customer_data[0].get("name")
    print(insert_products(token_dict, "PC", 23.1, 0))
    return render_template("customer.html", user=name) 