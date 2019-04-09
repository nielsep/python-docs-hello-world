
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    x = 50
    return x
