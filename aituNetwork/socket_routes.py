from flask import session, request
from flask_socketio import emit, send
from datetime import datetime
from aituNetwork.models import Users, Messages
from aituNetwork import db
from __main__ import socketio

from utils import auth_required

clients = dict()


@socketio.on('connect')
@auth_required
def connect():
    user_id = session['user'].id
    clients[user_id] = request.sid
    Users.update_user_info(user_id, dict(last_online='now'))


@socketio.on('disconnect')
@auth_required
def disconnect():
    user_id = session['user'].id
    Users.update_user_info(user_id, dict(last_online=str(datetime.now().replace(microsecond=0))))

    if clients.get(user_id):
        del clients[user_id]


@socketio.on('message')
def message(data: dict):
    chat_id = data['chat_id']
    from_user_id = data['from_user_id']
    user_id = data['user_id']
    message_text = data['message_text']

    new_message = Messages(chat_id=chat_id, user_id=from_user_id, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    if clients.get(user_id):
        send({'from_user_id': from_user_id, 'user_id': user_id, 'message': message_text}, to=clients[user_id])
