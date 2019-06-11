from flask import Flask
import requests


app = Flask(__name__)


@app.route('/')
def io_bound():
    resp = requests.get('http://localhost:8081')
    return resp.text
