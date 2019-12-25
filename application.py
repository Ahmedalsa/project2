import os

from flask import Flask, render_template, request, jsonify, Response
import random, json, time, datetime
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Arrays of channel names and registered users

# Dictionary of users & messages

# dictionary to track rooms, or private channels
# Rooms = {"dn:" displayname, "room": room}

# channel_messages

messages1 = {}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/logout", methods=["POST"])
def logout():
    return render_template("index.html")

@app.route("/flackchat", methods=["POST", "GET"])
def flackchat():
    user = request.form.get("displayname")
    return render_template("channels.html", name=user)

@app.route("/register")
def register():
    return 0

@socketio.on("submit channel")
def new_channel(data):
    channel = data["channel"]
    channel_list.append(channel)
    emit("announce channel", {"channel": channel}, broadcast=True)
    return 1

@app.route("/query_channels", methods=["POST"])
def query_channels():
    return jsonify({"success": True, "channel_list": channel_list})

@app.route("/query_users", methods=["POST"])
def query_users():
    return jsonify({"success": True, "active_users": user_list})

@app.route("/query_messages", methods=["POST"])
def fetch_messages():
    channel = request.form.get("channel")
    dn = request.form.get("displayname")
    msg_status = request.form.get("msg_type")

    if (msg_status == "PUBLIC"):
        my_msgs = channel_messages.get(channel)
    else:
        my_msgs = user_dm_list.get(channel)

    if (my_msgs):
        msglist = my_msgs['messages']
        if ((msg_status == "PUBLIC") or (channel == dn)):
            return jsonify({"success": True, "channel_msgs": msglist})
        else:
            all_msgs = []
            for msg in msglist:
                # return only messages matching dn
                if ((msg["user_from"] == dn) or (msg['user_to'] == dn)):
                    all_msgs.append(msg)
            return jsonify({"success": True, "channel_msgs": all_msgs})
    else:
        return jsonify({"success": False, "error_msg": "No messages"})

@socketio.on("send message")
def send(data):
    messages1.update(data)
    # room = data['room']
    emit("announce chat", messages1, broadcast=True)

@socketio.on('join')
def on_join(data):
    nickname = data['nickname']
    room = data['room']
    join_room(room)
    emit(nickname + ' has entered the room.', room=room)

@socketio.on('logout user')
def on_leave(data):
    username = data['displayname']
    print (f"username ", username, " logging out")
    room = Rooms[username]
    leave_room(room)
    del Rooms[username]
    emit("user logged out", {"username": username}, broadcast=True)

@socketio.on('leave')
def on_leave(data):
    username = data['displayname']
    print (f"username ", username, " logging out")
    room = Rooms[username]
    leave_room(room)
    del Rooms[username]
    emit("user logged out", {"username": username}, broadcast=True)


if __name__ == "__main__":
    app.run()
