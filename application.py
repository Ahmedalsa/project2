import os

from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
from decorators import login_required
import random, json, time, datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup")
def signup():
    return 0


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
