from flask import Blueprint, redirect

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return redirect('/login')

