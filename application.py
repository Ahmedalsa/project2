import os

from flask import Flask, render_template, request, jsonify, Response
from flask_socketio  import SocketIO, emit, send, emit, join_room, leave_room
from decorators import login_required
import random, json, time, datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

#following arrays are lists for active channels and users logged in
channel_arr =  ["General"]
user_arr = []

dm_list = {}

private_channles = {}

channelMessages = dict()


startup_message = {
  "channel": "General",
   "user_from": "Flack Bot",
   "user_to": "",
   "timestamp": now.strftime("%a %b %d %I:%M:%S %Y"),
   "msg_txt": "Welcome to Flack Messaging"}

#current datetime
current = datetime.datetime.now()

channel_messages = {
   "General": {
       'messages': [startup_message]
}}



@app.route("/")
def index():
    return render_template("index.html", channels=channel_arr)


@app.route("/login")
def login():
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":
        if len(username) < 1 or username is '':
            return render_template("error.html", message="username field is required!")
        if username in user_arr:
            return render_template("error.html", message="new username is required!")
        user_arr.append(username)
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

@app.route("/chat", methods=["POST", "GET"])
@login_required
def chat():
    return render_template("channels.html", name=user)

@app.route("/new_channel", methods=['GET','POST'])
@socketio.on("submit channel")
def new_channel():
    channel = data["channel"]
    channel_list.append(channel)
    emit("announce channel", {"channel": channel}, broadcast=True)
    return 1


@app.route("/users", methods=["POST", "GET"])
@login_required
def users():
    return jsonify({"success": True, "active_users": user_arr})


@app.route("/channels/<channel>", methods=["POST", "GET"])
@login_required
def channels():
    session['current_channel'] = channel

    if request.method == "POST":

        return redirect("/")
    else:
        return jsonify({"success": True, "channel_arr": channel_arr})

@app.route("/get_messages", methods=["POST", "GET"])
@login_required
def get_messages():
    channel = request.form.get("channel")
    status = request.form.get("message_status")
    displayname = request.form.get("displayname")

@socketio.on("join", namespace='/')
def on_join():
    room = session.get('current_channel')

    join_room(room)

    emit("status", {"joined": session.get('username'),
          "channel": room,
          "message": session.get('username') + "entered this chatroom"},
          room=room)

@socketio.on("join", namespace='/')
def on_leave():
    room = session.get('current_channel')

    leave_room(room)

    emit("status", {"joined": session.get('username'),
          "channel": room,
          "message": session.get('username') + "entered this chatroom"},
          room=room)


@socketio.on("submit message")
def new_message(message, timestamp):
    channel = data["channel"]
    user_from = data["user_from"]
    msg_txt = data["msg_txt"]
    timestamp = time.asctime( time.localtime( time.time() ) )


    msg = {"channel": channel,
           "user_from": user_from,
           "user_to": channel,
           "timestamp": timestamp,
           "msg_txt": msg_txt}
    if channel in channel_messages:
        # Public Channel with messages
        msgs = channel_messages[channel]
        msg["msg_type"] = "PUBLIC"
        if len(msgs['messages']) >= 100:
            del msgs['messages'][0]
        msgs['messages'].append(msg)
        emit("announce message", msg, broadcast=True)
        return jsonify ({"success": True, "msg_type": "PUBLIC"})
    else:
        if (not (channel in user_dm_list)):
            # public channel, first message
            msg["msg_type"] = "PUBLIC"
            channel_messages[channel] = {"channel": channel, "messages": [msg]}
            emit("announce message", msg, broadcast=True)
            return jsonify ({"success": True, "msg_type": "PUBLIC"})
        else:
            # private message
            msg["msg_type"] = "PRIVATE"
            if (channel in user_dm_list):
                for user in [user_from, channel]:
                    msgs = user_dm_list[user]
                    if len(msgs['messages']) >= 100:
                        del msgs['messages'][0]
                    msgs['messages'].append(msg)
            else:
                user_dm_list[user] = {"channel": channel, "messages": [msg]}
            print (f"NM: emit msg to ", user_from)
            msg["channel"] = channel
            emit("announce message", msg, room=Rooms[user_from])
            print (f"NM: emit msg to ", channel)
            msg["channel"] = user_from
            emit("announce message", msg, room=Rooms[channel])
            return jsonify ({"success": True, "msg_type": "PRIVATE"})


    if len(channelMessages[room]) > 100:
        emit({"user": session.get('username'),
              "timestamp": timestamp,
              "message": message},
              room=room)





if __name__ == "__main__":
    app.run()
