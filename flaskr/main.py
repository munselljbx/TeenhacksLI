import sys
from flask import Flask, render_template, request, redirect, Response
import random, json
from pathfinding import get_distances_from_rooms
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/receiver', methods = ['POST'])
def worker():
    data = request.get_json(force=True)
    print(get_distances_from_rooms(data["pathfindingdata"]))
    return "Hi there"

if __name__ == '__main__':
    app.run()
