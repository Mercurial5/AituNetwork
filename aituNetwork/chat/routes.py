from flask import request, session, render_template, redirect, url_for
from aituNetwork.chat import chat
from aituNetwork.models import Chats, UsersChats, Users, SeenMessages
from utils import auth_required


@chat.route('/')
@auth_required
def messages():
    user = session['user']
    chats = UsersChats.get_user_chats(user.id)
    chats = [Chats.get(chat.chat_id) for chat in chats]

    return render_template('messages.html', user=user, chats=chats)


@chat.route('/conversation')
@auth_required
def conversation():
    user = session['user']
    chat_user_id = int(request.values.get('chat_user_id'))

    chat_id = UsersChats.get_chat_between_users(user.id, chat_user_id)
    if chat_id is None:
        chat_id = Chats.create_chat()
        UsersChats.add_user_to_chat(chat_id, user.id)
        UsersChats.add_user_to_chat(chat_id, chat_user_id)

    return redirect(url_for('chat.chat', chat_id=chat_id))


@chat.route('/<chat_id>')
@auth_required
def chat(chat_id: int):
    user = session['user']

    new_messages = UsersChats.unread_messages_for_user(user.id, chat_id)
    new_messages = [SeenMessages(user_id=user.id, message_id=message.id) for message in new_messages]
    SeenMessages.update(new_messages)

    # user with whom you chat
    chat_user_id = UsersChats.get_second_chat_user(chat_id, user.id)
    chat_user = Users.get(chat_user_id)

    if not Chats.is_chat_exist(chat_id):
        return 'Chat does not exist'

    if not UsersChats.is_user_in_chat(user.id, chat_id):
        return 'User do not have access to this chat'

    if request.method == 'GET':
        return render_template('chat.html', user=user, chat_user=chat_user, chat_id=chat_id)
