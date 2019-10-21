import os

from flask import Flask
from flask_socketio import SocketIO, emit
from decorators import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():

@app.route("/")
def login():


@app.route("/")
@login_required
def logout():
