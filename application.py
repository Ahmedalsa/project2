import os

from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
from decorators import login_required
import random, json, time, datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

#following arrays are lists for active channels and users logged in
channel_arr ["General"]
user_arr = []

dm_list {}

private_channles = {}

#current datetime
current = datetime.datetime.now()

channel_messages = {
    "General": {
        'messages': [startup_message]
}}

startup_message = {
    "channel": "General",
    "user_from": "Flack Bot",
    "user_to": "",
    "timestamp": now.strftime("%a %b %d %I:%M:%S %Y"),
    "msg_txt": "Welcome to Flack Messaging"}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":
        if len(username) < 1 or username is '':
            return render_template("error.html", message="username field is required!")
        if username in usersLogged:
            return render_template("error.html", message="new username is required!")
        usersLogged.append(username)
        session['username'] = username

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    usersLogged.remove(session['username'])
    session.clear()
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
