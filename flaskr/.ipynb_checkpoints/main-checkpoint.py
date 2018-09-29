#sample code
import numpy as np
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

npTest = np.zeros((3, 4))
