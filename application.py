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
channelsList=[]
privateMessages={}
usersList={}
limit=100


@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def connect():
    emit("load channels",{'channels':channels})

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

@socketio.on('new channel')
def new_channel(data):
    error=""
    if data["channel"] in channelsList or data['channel']=="General":
        error="Channel already exist. Try again."
    elif data["channel"][0].isdigit():
        error="Channel name cannot start with a number"
    elif ' ' in data['channel']:
        error="Channel name can't contain space"
    else:
        channelsList.append(data['channel'])
        #create place for future messages
        channels[data["channel"]]=[]
    emit("add channel",{'channel':data["channel"],'error':error})

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
def join(data):
    room = data["channel"]
    join_room(room)
    message={'text':data["mymessage"],'username':data['username'],"time":data['time']}
    channels[data["channel"]].append(message)
    if (len(channels[data["channel"]])>limit):
        channels[data["channel"]].pop(0)
    emit("joined",{'channels':channels},room=room)

@socketio.on('leave')
def leave(data):
    room = data["channel"]
    leave_room(room)
    message={'text':data["mymessage"],'username':data['username'],"time":data['time']}
    channels[data["channel"]].append(message)
    if (len(channels[data["channel"]])>limit):
        channels[data["channel"]].pop(0)
    emit("left",{'channels':channels},room=room)

@socketio.on('leave')
def on_leave(data):
    nickname = data['nickname']
    room = data['room']
    leave_room(room)
    emit(nickname + ' has left the room.', room=room)

@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])


if __name__ == "__main__":
    app.run()
