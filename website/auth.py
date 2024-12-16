from flask import Blueprint, render_template, redirect, flash, url_for
import json
from moloni import *
from sap import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    with open("tokens_moloni.json", "r") as tokens_moloni_file:
        token_dict = json.load(tokens_moloni_file)
    if request.method == 'POST':
        email = request.form.get('email')
        customer = get_customer_by_email(token_dict, email).json()
        if not customer:
            flash('Email not registered', category="error")
        else:
            return redirect(url_for('customer.menu', c=email))

    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/register', methods=['GET','POST'])
def register():
    with open("tokens_moloni.json", "r") as tokens_moloni_file:
        token_dict = json.load(tokens_moloni_file)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        nif = request.form.get('nif')
        address = request.form.get('address')
        zip_code = request.form.get('zip_code')
        city = request.form.get('city')
        next_number = get_next_customer(token_dict).get("number")
        customeremail = get_customer_by_email(token_dict, email).json()
        customernif = get_customer_by_nif(token_dict, nif).json()
        if not customeremail:
            if not customernif:
                insert_customer(token_dict, name, email, nif, address, zip_code, city, next_number)
                insert_customer_sap(name)
                flash('Accounted registered successfully', category="success")
            else:
                flash('NIF already registered', category="error")
        else:
            flash('Email already registered', category="error")

    return render_template("register.html")