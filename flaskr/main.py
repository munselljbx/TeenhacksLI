import sys
from flask import Flask, render_template, request, redirect, Response
import random, json
from pathfinding import get_distances_from_rooms
from gen_schedules import optimize_schedules
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/receiver', methods = ['POST'])
def worker():
    data = request.get_json(force=True)
    dist = get_distances_from_rooms(data["pathfindingdata"])
    print(data["student_info"][:-1])
    print(data["roomdata"])
    print (optimize_schedules(data["student_info"][:-1], data["roomdata"], dist))
    return "Hi there"

if __name__ == '__main__':
    app.run()
