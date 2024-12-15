from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta


USERNAME = "a104161@alunos.uminho.pt"
DEV_ID = "251975622_TESTES_API_UM"
DEV_PASSWORD = "RLTF.hFra87d3Un"
CLIENT_SECRET = "117367f336141e5908b20ac59cae8172e735af41"
COMPANY_ID = 323135
CATEGORY_ID = 8555101

def get_date_time():
    current_datetime = datetime.now()
    return current_datetime.strftime('%Y-%m-%d %H:%M:%S')


def get_customer_count(token_dict):
    url = f"https://api.moloni.pt/v1/customers/count/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return requests.post(url, headers=headers, data=payload)

def insert_customer(token_dict, name, email, nif, address, zip_code, city, number):
    url = f"https://api.moloni.pt/v1/customers/insert/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "vat": nif,
        "number": number,
        "name": name,
        "language_id": 1,
        "address": address,
        "zip_code": zip_code,
        "city": city,
        "country_id": 1,
        "email": email,
        "salesman_id": 0,
        "price_class_id": 0,
        "maturity_date_id": 0,
        "payment_day": 0,
        "discount": 0,
        "credit_limit": 0,
        "payment_method_id": 0,
        "delivery_method_id": 2517293,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded' 
    }
    response = requests.post(url, headers=headers, data=payload)


def get_customer_by_email(token_dict, email):
    url = f"https://api.moloni.pt/v1/customers/getByEmail/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "email": email
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)
    return response

def get_customer_by_nif(token_dict, nif):
    url = f"https://api.moloni.pt/v1/customers/getByVat/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "vat": nif
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)
    return response

def insert_products(token_dict, name, price, initialstock):
    url = f"https://api.moloni.pt/v1/products/insert/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "category_id": CATEGORY_ID,
        "type": 1,
        "reference": get_next_reference(token_dict).get("reference"), # Create different refferences
        "name": name,
        "price": price,
        "has_stock": 1,
        "at_product_category": "M",
        "stock": initialstock,
        "unit_id": 1234,
        "exemption_reason": "xD"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)

def get_next_reference(token_dict):
    url = f"https://api.moloni.pt/v1/products/getNextReference/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return requests.post(url, headers=headers, data=payload).json()

def get_next_customer(token_dict):
    url = f"https://api.moloni.pt/v1/customers/getNextNumber/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(url, headers=headers, data=payload).json()

def get_all_products(token_dict):
    url = f"https://api.moloni.pt/v1/products/getAll/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "category_id": CATEGORY_ID,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(url, headers=headers, data=payload).json()

def stock_movement(token_dict, product_id, quantity):
    url = f"https://api.moloni.pt/v1/productStocks/insert/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "product_id": product_id,
        "movement_data": get_date_time(),
        "qty": quantity
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(url, headers=headers, data=payload).json()

def get_prod_by_name(token_dict, product_name):
    url = f"https://api.moloni.pt/v1/products/getByName/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "name": product_name,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(url, headers=headers, data=payload).json()



def generate_document(token_dict, product, customer_id): #simplified
    url = f"https://api.moloni.pt/v1/internalDocuments/insert/?access_token={token_dict["access_token"]}&json=true"
    current_date = datetime.now()
    expiration_date = current_date + relativedelta(months=1)
    current_date = current_date.strftime("%Y-%m-%d")
    expiration_date = expiration_date.strftime("%Y-%m-%d")
    payload = {
        "company_id": COMPANY_ID,
        "date": current_date,
        "expiration_date": expiration_date,
        "document_set_id": 762961,
        "customer_id": customer_id,
        "status": 1,
        "products": [
                {
                    "product_id": product.get("product_id"),
                    "name": product.get("name"),
                    "qty": 1,
                    "price": product.get("price"),
                    "exemption_reason": "M01"
                }
            ]
        }
    # Headers to specify the content type as JSON
    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(url, json=payload, headers=headers).json()
    
def get_doc(token_dict, document_id):
    url = f"https://api.moloni.pt/v1/documents/getOne/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "document_id": document_id
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(url, headers=headers, data=payload).json()

def get_pdf_link(token_dict, document_id):
    url = f"https://api.moloni.pt/v1/documents/getPDFLink/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID,
        "document_id": document_id
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(url, headers=headers, data=payload).json()
