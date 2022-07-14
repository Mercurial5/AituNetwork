from flask import request, redirect, url_for, session, flash
from better_profanity import profanity

from aituNetwork.models import Posts, PostLikes, PostComments, Users, Admins
from aituNetwork.crud import crud
from utils import auth_required


@crud.route('/add/post', methods=['POST'])
@auth_required
def add_post():
    post_content = request.form.get('post-content')
    post_content = profanity.censor(post_content)

    Posts.add_post(session['user'].id, post_content)

    flash('Your post is added!', 'success')
    return redirect(url_for('users.profile', slug=session['user'].slug))


@crud.route('/delete/post/<post_id>')
@auth_required
def delete_post(post_id):
    user = session['user']
    post = Posts.get(post_id)
    profile_user = Users.get(post.author_id)

    if user.id != post.author_id and not Admins.is_admin(user.id):
        flash('You don\'t access', 'danger')
        return redirect(url_for('users.profile', slug=profile_user.slug))

    Posts.delete_post(post_id)
    PostLikes.delete_likes_from_post(post_id)
    PostComments.delete_comments_from_post(post_id)

    return redirect(url_for('users.profile', slug=profile_user.slug))
