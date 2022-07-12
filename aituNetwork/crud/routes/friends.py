from flask import request, redirect, url_for
from aituNetwork.crud import crud
from aituNetwork.models import Users, Friends

from utils import auth_required


@crud.route('/add/friend')
@auth_required
def add_friend():
    user_id = request.values.get('user_id')
    friend_id = request.values.get('friend_id')

    Friends.add_friend(user_id, friend_id)

    return redirect(url_for('users.profile', slug=Users.query.get(friend_id).slug))


@crud.route('/delete/friend')
@auth_required
def delete_friend():
    user_id = request.values.get('user_id')
    friend_id = request.values.get('friend_id')

    Friends.remove_friend(user_id, friend_id)

    return redirect(url_for('users.profile', slug=Users.query.get(friend_id).slug))
