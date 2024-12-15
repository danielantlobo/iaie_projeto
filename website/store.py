from flask import Blueprint, render_template, redirect, flash
import json
from sap import *
from moloni import *

SECRET_KEY = "store"

store = Blueprint('store', __name__)

@store.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        secret_key = request.form.get('secret_key')
        if secret_key == SECRET_KEY:
            return redirect("/store/home")
        else:
            flash('Secret key not registered', category="error")
    return render_template("login_store.html")

@store.route('/home', methods=['GET','POST'])
def menu():
    if request.method == 'POST':
        pass
    return render_template("store.html")
