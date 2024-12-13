from flask import Blueprint, render_template, redirect, flash
import json
from moloni import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    with open("tokens_moloni.json", "r") as tokens_moloni_file:
        token_dict = json.load(tokens_moloni_file)
    if request.method == 'POST':
        email = request.form.get('email')
        customer = get_customer_by_email(token_dict, email).json()
        if not customer:
            flash('Email não registado', category="error")
        else:
            return redirect("/")


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
        count = get_customer_count(token_dict).json()
        customer = get_customer_by_email(token_dict, email).json()
        if not customer:
            insert_customer(token_dict, name, email, nif, address, zip_code, city, count)
            print(count)
            flash('Conta registada com sucesso', category="success")
        else:
            flash('Esse email já está registado', category="error")

    return render_template("register.html")