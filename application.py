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

@socketio.on('submit to all')
def submit_to_all(data):
    message={'text':data["mymessage"],'username':data['username'],"time":data['time']}
    channels['General'].append(message)
    if (len(channels['General'])>limit):
        channels['General'].pop(0)
    emit("announce to all",{'channels':channels},broadcast=True)

@socketio.on('submit to room')
def submit_to_room(data):
    room = data["channel"]
    message={'text':data["mymessage"],'username':data['username'],"time":data['time']}
    channels[data["channel"]].append(message)
    if (len(channels[data["channel"]])>limit):
        channels[data["channel"]].pop(0)
    emit("announce to room",{'channels':channels},room=room)

@socketio.on('new username')
def new_username(data):
    username=""
    error=""
    if data['username'] in usersList:
        error="Username already exist. Try again"
    else:
        usersList[data['username']]=request.sid
        username=data["username"]
    emit("add username",{"username":username,'error':error})

@socketio.on('come back to general')
def come_back_to_general():
    emit("announce to all",{'channels':channels},broadcast=True)


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

@socketio.on('update users channels')
def update_users_channels(data):
    channel=data['channel']
    emit("update channels",{'channel':channel},broadcast=True)

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

@socketio.on('submit to room')
def submit_to_room(data):
    room = data["channel"]
    message={'text':data["mymessage"],'username':data['username'],"time":data['time']}
    channels[data["channel"]].append(message)
    if (len(channels[data["channel"]])>limit):
        channels[data["channel"]].pop(0)
    emit("announce to room",{'channels':channels},room=room)

@socketio.on('new username')
def new_username(data):
    username=""
    error=""
    if data['username'] in usersList:
        error="Username already exist. Try again"
    else:
        usersList[data['username']]=request.sid
        username=data["username"]
    emit("add username",{"username":username,'error':error})


@socketio.on('private')
def private(data):
    message={'text':data["mymessage"],'username':data['username'],"time":data['time']}
    room=data['username']+data['username2']
    if data['username'] not in privateMessages:
        privateMessages[data['username']]={}
    if data['username2'] not in privateMessages:
        privateMessages[data['username2']]={}
    if data['username'] not in privateMessages[data['username2']]:
        privateMessages[data['username2']][data['username']]=[]
    if data['username2'] not in privateMessages[data['username']]:
        privateMessages[data['username']][data['username2']]=[]
    privateMessages[data['username2']][data['username']].append(message)
    privateMessages[data['username']][data['username2']].append(message)
    if (len(privateMessages[data['username2']][data['username']])>limit):
        privateMessages[data['username2']][data['username']].pop(0)
    if (len(privateMessages[data['username']][data['username2']])>limit):
        privateMessages[data['username']][data['username2']].pop(0)
    #assign two users into room
    socketio.server.enter_room(usersList[data['username2']], room)
    socketio.server.enter_room(request.sid, room)
    emit('private room',{'privateMessages':privateMessages,'sender':data['username'],'receiver':data['username2']},room=room)

@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])


if __name__ == "__main__":
    app.run()
