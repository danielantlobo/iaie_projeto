from flask import Flask, render_template, request, redirect
import requests
import json

AUTH = 'Basic TEVBUk4tMDM0OiNEYW5pMTAxMw=='

def get_token_sap():
    url = "https://s53.gb.ucc.cit.tum.de/sap/opu/odata/sap/MD_C_PRODUCT_MAINTAIN_SRV/C_Product?$format=json&$filter=CreatedByUser eq 'LEARN-034'"

    payload = {}
    headers = {
        'sap-client': '317',
        'X-CSRF-Token': 'fetch',
        'Authorization': AUTH,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.headers.get('x-csrf-token')

def add_product(name, quantity):
    token = get_token_sap()
    url = "https://s53.gb.ucc.cit.tum.de/sap/opu/odata/sap/MD_C_PRODUCT_MAINTAIN_SRV/C_Product"

    payload = json.dumps({
    "ProductType": "FERT",
    "ProductDescription": name,
    "BaseUnit": "EA",
    "ManufacturerNumber": f"{quantity}"
    })
    headers = {
    'sap-client': '317',
    'X-CSRF-Token': token,
    'Content-Type': 'application/json',
    }

    return requests.request("POST", url, headers=headers, data=payload)

def deduct_product(name, quantity):
    token = get_token_sap()
    