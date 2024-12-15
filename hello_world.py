from flask import Flask, render_template, request, redirect
import requests
import threading
import time
import json

USERNAME = "a104161@alunos.uminho.pt"
DEV_ID = "251975622_TESTES_API_UM"
DEV_PASSWORD = "RLTF.hFra87d3Un"
CLIENT_SECRET = "117367f336141e5908b20ac59cae8172e735af41"
COMPANY_ID = 323135

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lsdasaldsadmksaifdfirefbewqu'

def get_token():
    url = f"https://api.moloni.pt/v1/grant/?grant_type=password&client_id={DEV_ID}&client_secret={CLIENT_SECRET}&username={USERNAME}&password={DEV_PASSWORD}"
    response = requests.request("GET", url)
    data = response.json()
    # Criar dicionário com a access token e refresh token
    token_dict = {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token")
    }
    return token_dict


def refresh_token(token_dict):
    while True:
        time.sleep(3550)
        url = f"https://api.moloni.pt/v1/grant/?grant_type=refresh_token&client_id={DEV_ID}&client_secret={CLIENT_SECRET}&refresh_token={token_dict["refresh_token"]}"
        response = requests.request("GET", url)
        data = response.json()
        token_dict["access_token"] = data.get("access_token")
        token_dict["refresh_token"] = data.get("refresh_token")

def get_all_customers(token_dict):
    url = f"https://api.moloni.pt/v1/customers/getAll/?access_token={token_dict["access_token"]}"
    payload = {
        "company_id": COMPANY_ID
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

def get_customer_count(token_dict):
    url = f"https://api.moloni.pt/v1/customers/count/?access_token={token_dict['access_token']}&json=true"
    
    # Body content
    payload = {
        "company_id": COMPANY_ID
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
    }
    
    # GET request with body
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    return response


def insert_customer(token_dict):
    url = f"https://api.moloni.pt/v1/customers/insert/?access_token={token_dict["access_token"]}"
    response = get_customer_count(token_dict).json()
    payload = {
        "company_id": COMPANY_ID,
        "vat": "251975622",
        "number": response.get("count"),
        "name": "Daniel",
        "language_id": 1,
        "address": "Rua S.Tiago",
        "zip_code": "3213-321",
        "city": "Guimarães",
        "country_id": 1,
        "email": "daniel@gmail.com",
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
    print(response.status_code)
    print(response.text)


@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():

    name = request.form.get('name')
    email = request.form.get('email')
    nif = request.form.get('nif')

    print(email, name, nif, sep="\n")


# Ligar o servidor
if __name__ == '__main__':
    # Receber a access token do moloni
    token_dict = get_token()
    # Criar uma thread para ir dando update à acess token antes dela expirar
    thread = threading.Thread(target=get_token, args=(token_dict,))
    print(get_customer_count(token_dict))

    app.run(host="127.0.0.1", port=5050)

