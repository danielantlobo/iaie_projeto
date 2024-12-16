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
            return redirect("/supplier/home")
        else:
            flash('Secret key not registered', category="error")
    return render_template("login_supplier.html")

@supplier.route('/home', methods=['GET','POST'])
def menu():

    if request.method == 'POST':
        product_name = request.form.get('name')
        product_quantity = request.form.get('quantity')
        price = request.form.get('price')
        add_product(product_name, product_quantity, price)
        token = get_token_sap()
    
    products = get_products().get("d").get("results")
    products_relevant = []
    for product in products:
        products_relevant.append({"name": product.get("ProductDescription"), "quantity": product.get("ManufacturerNumber"), "price": product.get("MaterialVolume")})

    return render_template("supplier.html", products=products_relevant)