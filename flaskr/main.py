import sys
from flask import Flask, render_template, request, redirect, Response
import random, json
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/receiver', methods = ['POST'])
def worker():
    data = request.get_json(force=True)
    print(data)
    return "Hi there"

if __name__ == '__main__':
    app.run()
