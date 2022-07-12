from flask import request, session, redirect, url_for
from aituNetwork.models import Comments, PostComments, Admins
from aituNetwork.crud import crud
from utils import auth_required


@crud.route('/add/comment', methods=['POST'])
@auth_required
def add_comment():
    post_id = int(request.form.get('post_id'))
    author_id = session['user'].id
    text = request.form.get('text')

    comment = Comments.create_comment(author_id, text)
    PostComments.add_comment_to_post(post_id, comment.id)

    return 'ok'


@crud.route('/delete/comment')
@auth_required
def delete_comment():
    comment_id = request.values.get('comment_id')

    user = session['user']
    comment = Comments.get(comment_id)

    if comment is None:
        return 'Comment not found'

    if comment.user_id != user.id and not Admins.is_admin(user.id):
        return 'You don\'t have an access'

    Comments.delete_comment(comment_id)
    PostComments.delete_comment_from_post(comment_id)

    return redirect(url_for('main.home'))
