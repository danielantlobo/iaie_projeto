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

    return requests.request("GET", url, headers=headers, data=payload).headers

def add_product(name, quantity, price):
    url = "https://s53.gb.ucc.cit.tum.de/sap/opu/odata/sap/MD_C_PRODUCT_MAINTAIN_SRV/C_Product"

    headers = get_token_sap()
    cookies = get_cookies_from_headers(headers)

    payload = json.dumps({
        "ProductType": "FERT",
        "ProductDescription": name,
        "BaseUnit": "EA",
        "ManufacturerNumber": quantity,
        "MaterialVolume": price
    })
    headers = {
        'sap-client': '317',
        'X-CSRF-Token': headers.get("x-csrf-token"),
        'Authorization': AUTH,
        'Content-Type': 'application/json',
        'Cookie': cookies
    }

    return requests.request("POST", url, headers=headers, data=payload)


def get_products():
    url = "https://s53.gb.ucc.cit.tum.de/sap/opu/odata/sap/MD_C_PRODUCT_MAINTAIN_SRV/C_Product?$format=json&$filter=CreatedByUser eq 'LEARN-034'"

    payload = {}
    headers = {
        'sap-client': '317',
        'Authorization': AUTH,
    }

    return requests.request("GET", url, headers=headers, data=payload).json()

def insert_customer_sap(name):

    headers = get_token_sap()
    cookies = get_cookies_from_headers(headers)

    url = "https://s53.gb.ucc.cit.tum.de/sap/opu/odata/sap/MD_BUSINESSPARTNER_SRV/C_BusinessPartner"

    payload = json.dumps({
        "BusinessPartnerCategory": "1",
        "FullName": name,
        "BusinessPartnerIsBlocked": False
    })
    headers = {
        'X-CSRF-Token': headers.get("x-csrf-token"),
        'Cookie': cookies,
        'sap-client': '317',
        'Content-Type': 'application/json',
        'Authorization': AUTH
    }

    response = requests.request("POST", url, headers=headers, data=payload)


def get_cookies_from_headers(headers):
    # Get the 'set-cookie' header from the response headers
    set_cookie = headers.get('set-cookie', '')
    
    # Split the cookie string into individual cookies
    cookies = set_cookie.split(', ')
    
    # Extract relevant cookies and format them
    cookie_dict = {}
    for cookie in cookies:
        if '=' in cookie:
            key, value = cookie.split(';')[0].split('=', 1)
            cookie_dict[key] = value
    
    # Reformat the cookies into the desired string
    formatted_cookies = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])
    return formatted_cookies