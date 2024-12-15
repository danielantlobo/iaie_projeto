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
    #insert_products(token_dict, "Macbook Air 13'' M2", 1423.1, 10) # Preciso dos dados do SAP
    products_all = get_all_products(token_dict)
    products_relevant = []
    for product in products_all:
        products_relevant.append({"name": product.get("name"), "price": product.get("price"), "quantity": product.get("stock")})


    purchased_product = None
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')
        product = get_prod_by_name(token_dict, product_name)[0]
        product_id = product.get("product_id")

        stock_mov = stock_movement(token_dict, product_id, -1)
        generate_new_document = generate_document(token_dict, product, customer_data[0].get("customer_id"))
        print(generate_new_document)
        pdf_link = get_pdf_link(token_dict, generate_new_document.get("document_id")).get("url")

        flash(f'You bought {product_name} for {product_price}€ ({pdf_link})', category="success")
        return redirect(url_for('customer.menu', c=email))
    
    return render_template("customer.html", user=name, products=products_relevant)