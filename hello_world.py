from flask import Flask, jsonify, request
import requests
import random

app = Flask(__name__)

# Ligar o servidor
if __name__ == '__main__':
    register_producer() # Registar produtor
    app.run(host="127.0.0.1", port=6666)