from website import create_app
from flask import Flask, render_template, request, redirect
import json
import requests
import threading
import time

USERNAME = "a104161@alunos.uminho.pt"
DEV_ID = "251975622_TESTES_API_UM"
DEV_PASSWORD = "RLTF.hFra87d3Un"
CLIENT_SECRET = "117367f336141e5908b20ac59cae8172e735af41"
COMPANY_ID = 323135

def get_token():
    url = f"https://api.moloni.pt/v1/grant/?grant_type=password&client_id={DEV_ID}&client_secret={CLIENT_SECRET}&username={USERNAME}&password={DEV_PASSWORD}"
    response = requests.request("GET", url)
    data = response.json()
    # Criar dicionário com a access token e refresh token
    token_dict = {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token")
        
    }
    with open("tokens_moloni.json", "w") as tokens_moloni_file:
        json.dump(token_dict, tokens_moloni_file, indent=4)
    return token_dict

def refresh_token(token_dict):
    while True:
        time.sleep(3550)
        url = f"https://api.moloni.pt/v1/grant/?grant_type=refresh_token&client_id={DEV_ID}&client_secret={CLIENT_SECRET}&refresh_token={token_dict["refresh_token"]}"
        response = requests.request("GET", url)
        data = response.json()
        token_dict["access_token"] = data.get("access_token")
        token_dict["refresh_token"] = data.get("refresh_token")
        with open("tokens_moloni.json", "w") as tokens_moloni_file:
            json.dump(token_dict, tokens_moloni_file, indent=4)

app = create_app()

if __name__ == '__main__':
    # Receber a access token do moloni
    token_dict = get_token()
    # Criar uma thread para ir dando update à acess token antes dela expirar
    thread = threading.Thread(target=get_token, args=(token_dict,))

    app.run(debug=True)