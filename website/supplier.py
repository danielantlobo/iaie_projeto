from flask import Blueprint, render_template, redirect, flash
import json
from sap import *

SECRET_KEY = "supplier"

supplier = Blueprint('supplier', __name__)

@supplier.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        secret_key = request.form.get('secret_key')
        if secret_key == SECRET_KEY:
            print("hello")
        else:
            flash('Secret key not registered', category="error")
    return render_template("login_supplier.html")
