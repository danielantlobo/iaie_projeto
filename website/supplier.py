from flask import Blueprint, render_template, redirect, flash
import json
from sap import *

supplier = Blueprint('supplier', __name__)

@supplier.route('/login', methods=['GET','POST'])
def login():
    
    return render_template("login_supplier.html")
