from flask import request, send_file, render_template, session
from datetime import datetime

from aituNetwork.models import PostLikes, Users, Messages, Comments, Posts
from aituNetwork.utils import utils
from utils import picturesDB

from utils import auth_required


@utils.route('/get-picture/<filename>', methods=['GET'])
def get_picture(filename: str):
    path = picturesDB.get_picture_path('profile-pictures', filename)
    return send_file(path, mimetype='image/gif')


@utils.route('/like', methods=['POST'])
@auth_required
def like():
    post_id = int(request.form.get('post_id'))
    user_id = session['user'].id

    PostLikes.add(user_id, post_id)

    return dict(status='ok')


@utils.route('/unlike', methods=['POST'])
@auth_required
def unlike():
    post_id = int(request.form.get('post_id'))
    user_id = session['user'].id

    PostLikes.remove(user_id, post_id)

    return dict(status='ok')


@utils.route('/generate-message', methods=['POST'])
def generate_message():
    user_id = int(request.form.get('user_id'))
    message = request.form.get('message')

    now = datetime.now().replace(microsecond=0)

    return render_template('message.html', user=Users.get(user_id), message=message, time=now)


@utils.route('/get-messages', methods=['POST'])
def get_messages():
    chat_id = int(request.form.get('chat_id'))
    offset = int(request.form.get('offset'))
    limit = int(request.form.get('limit'))
    with_html = request.form.get('with_html')

    messages = Messages.get_messages(chat_id, offset, limit)

    html = None
    if with_html:
        html = [render_template('message.html', user=Users.get(message.user_id), message=message.message, time=message.created) for message in
                messages]

    return dict(messages=[message.serialize() for message in messages], html=html)


@utils.route('/generate-comment', methods=['POST'])
def generate_comment():
    user_id = int(request.form.get('user_id'))
    author_id = int(request.form.get('author_id'))
    post_id = int(request.form.get('post_id'))
    text = request.form.get('text')

    user = Users.get(user_id)
    author = Users.get(author_id)
    comment = Comments.create_comment(author_id, text)
    post = Posts.get(post_id)

    return render_template('comment.html', user=user, author=author, comment=comment, post=post)
