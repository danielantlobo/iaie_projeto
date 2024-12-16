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
    with open("tokens_moloni.json", "r") as tokens_moloni_file:
        token_dict = json.load(tokens_moloni_file)
    
    products_all = get_all_products(token_dict)
    products_relevant = []
    for product in products_all:
        products_relevant.append({"name": product.get("name"), "price": product.get("price"), "quantity": product.get("stock")})

    products_supplier = get_products().get("d").get("results")
    products_supplier_rel = []
    for product in products_supplier:
        products_supplier_rel.append({"name": product.get("ProductDescription"), "quantity": product.get("ManufacturerNumber"), "price": product.get("MaterialVolume")})

    if request.method == 'POST':
        product_name = request.form.get('name')
        product_quantity = request.form.get('quantity')
        price = request.form.get('price')
        found_sup = False
        found_mol = False

        for product in products_supplier_rel:
            if product.get("name") == product_name:
                found_sup = True


        if found_sup:
            product = get_prod_by_name(token_dict, product_name)
            if product:
                product_id = product[0].get("product_id")
                stock_movement(token_dict, product_id, product_quantity)
                flash(f'You added {product_quantity} new {product_name}', category="success")
                return redirect('/store/home')
            else:
                insert_products(token_dict, product_name, price, product_quantity)
                flash(f'You added {product_quantity} new {product_name}', category="success")
                return redirect('/store/home')
        else:
            flash(f'Supplier does not have this product in stock', category="error")

    return render_template("store.html", products=products_relevant, products_sap=products_supplier_rel)
