from flask import session, redirect, url_for
from aituNetwork.models import Users, Admins, Friends, Chats, UsersChats, ProfilePictures
from aituNetwork.models import Messages, Posts, PostLikes, Comments, PostComments, db
from aituNetwork.crud import crud
from utils import auth_required
from utils import picturesDB


@crud.route('/delete/user/<user_id>')
@auth_required
def delete_user(user_id: int):
    user = session['user']
    profile_user = Users.get(user_id)

    if profile_user is None:
        return 'User not found'

    if not Admins.is_admin(user.id):
        return redirect(url_for('users.profile', slug=profile_user.id))

    # delete from Users
    Users.delete_user(profile_user.id)

    # delete from Friends
    Friends.delete_friends_for_deleted_user(user_id)

    # delete from UsersChats/Chats/Messages
    chat_list = UsersChats.delete_chats_for_deleted_user(user_id)
    [Chats.delete_chat(chat.chat_id) for chat in chat_list]
    [Messages.delete_messages_in_chat(chat.chat_id) for chat in chat_list]

    # delete from Posts/PostLikes
    posts_id_list = Posts.delete_posts_for_deleted_user(user_id)
    PostLikes.delete_likes_for_deleted_user(user_id, posts_id_list)

    # delete from Comments/PostComments
    comments_id_list = Comments.delete_for_deleted_user(user_id)
    [PostComments.delete_comment_from_post(comment_id[0]) for comment_id in comments_id_list]

    # delete from ProfilePictures
    pictures = ProfilePictures.delete_pictures_for_deleted_user(user_id)
    [picturesDB.delete_picture('profile-pictures', picture.name) for picture in pictures]

    db.session.commit()

    return 'User was deleted'
