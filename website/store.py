from flask import Blueprint, render_template, redirect, flash
import json
from sap import *
from moloni import *

store = Blueprint('store', __name__)

@store.route('/login', methods=['GET','POST'])
def login():
    
    return render_template("login_store.html")
