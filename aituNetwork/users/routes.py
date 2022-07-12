from flask import request, render_template, session
from flask import redirect, url_for, flash
from passlib.hash import sha256_crypt
from aituNetwork.users import users
from aituNetwork.models import Users, ProfilePictures, Friends, Posts, UsersChats, Chats, Cities, EduPrograms, Admins, \
    Messages, PostLikes, Comments, PostComments
from aituNetwork import db
from utils import picturesDB, auth_required

import requests


@users.route('/profile/<slug>', methods=['GET'])
@auth_required
def profile(slug: str):
    profile_user = Users.query.filter_by(slug=slug).first()

    if profile_user is None:
        return 'user is not found'

    profile_picture = ProfilePictures.get_profile_picture(profile_user.id)
    if profile_picture:
        profile_user.profile_picture = profile_picture.name

    posts = Posts.get_posts(profile_user.id)

    user = session['user']

    friend_status = Friends.get_friend_status(user.id, profile_user.id)
    friend_list = Friends.get_friend_list(profile_user.id)[:6]

    return render_template('profile.html', user=user, profile_user=profile_user, friend_status=friend_status,
                           posts=posts, friend_list=friend_list)


@users.route('/friends/<user_id>')
@auth_required
def friends(user_id):
    friends_of = Users.get(user_id)
    friend_list = Friends.get_friend_list(friends_of.id)

    return render_template('friends.html', user=session['user'], friends_of=friends_of, friend_list=friend_list)


@users.route('/messages')
@auth_required
def messages():
    user = session['user']
    chats = UsersChats.get_user_chats(user.id)
    chats = [Chats.get(chat.chat_id) for chat in chats]

    return render_template('messages.html', user=user, chats=chats)


@users.route('/settings', defaults={'user_id': None}, methods=['GET', 'POST'])
@users.route('/settings/<user_id>', methods=['GET', 'POST'])
@auth_required
def settings(user_id: int):
    user = session['user']

    if user_id is None:
        user_id = user.id

    target_user = Users.get(user_id)

    if user.id != user_id and not Admins.is_admin(user.id):
        flash('You don\'t access', 'danger')
        return redirect(url_for('users.profile', slug=Users.get(user_id).slug))

    edu_programs = EduPrograms.get_edu_programs()
    cities = Cities.get_cities()

    if request.method == 'GET':
        return render_template('settings.html', user=target_user, cities=cities, edu_programs=edu_programs)

    picture = request.files.get('profile-picture')
    if picture:
        picture_name = picturesDB.add_picture('profile-pictures', picture)
        profile_picture = ProfilePictures(user_id=target_user.id, name=picture_name)
        db.session.add(profile_picture)

    slug = request.form.get('slug')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    about_me = request.form.get('about-me')
    birthday = request.form.get('birthday', None)
    birthday = None if birthday == '' else birthday
    city = request.form.get('city')
    course = request.form.get('course')
    edu_program = request.form.get('edu-program')
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')

    if password != '':
        if password != password_confirm:
            flash('Passwords does not match')
            return redirect(url_for('users.settings'))
        password = sha256_crypt.hash(password)
    else:
        password = target_user.password

    if Users.is_slug_taken(slug) and slug != target_user.slug:
        flash('Slug is already taken.', 'danger')
        return redirect(url_for('users.settings'))

    update_info = dict(slug=slug, first_name=first_name, last_name=last_name, about_me=about_me, birthday=birthday,
                       city=city, course=course, edu_program=edu_program, password=password)
    Users.update_user_info(target_user.id, update_info)

    if user.id == target_user.id:
        session['user'] = Users.query.get(target_user.id)

    flash('Info was updated', 'success')
    return redirect(url_for('users.settings'))


@users.route('/movies', methods=['GET', 'POST'])
@auth_required
def movies_search():
    url_search = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword"
    url_top = "https://kinopoiskapiunofficial.tech/api/v2.1/films/top"
    headers = {'X-API-KEY': '1af58e0d-6f44-4ec0-9a57-5a51c892f857', 'Content-Type': 'application/json'}
    search_text = request.values.get("search-text")
    if not search_text:
        params = {"type": "TOP_100_POPULAR_FILMS"}
        r = requests.get(url_top, params=params, headers=headers).json()
    else:
        params = {"keyword": search_text}
        r = requests.get(url_search, params=params, headers=headers).json()
        films_list = []
        for field in r['films']:
            films_list.append(field)
    return render_template('movies.html', user=session['user'], films=r['films'], search_text=search_text)


@users.route('/movies/<filmId>', methods=['GET', 'POST'])
@auth_required
def movies(filmId):
    api_url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/" + filmId
    headers = {'X-API-KEY': '1af58e0d-6f44-4ec0-9a57-5a51c892f857', 'Content-Type': 'application/json'}
    params = {"id": filmId}
    r = requests.get(api_url, headers=headers, params=params).json()
    return render_template('movie_player.html', user=session['user'], film=r['data'])


@users.route('/find-friends')
@auth_required
def find_friends():
    user = session['user']

    search = request.values.get('search', '')
    city = int(request.values.get('city', 0))
    course = int(request.values.get('course', 0))
    edu_program = int(request.values.get('edu_program', 0))

    users_list = Users.get_users_for_new_friends_list(user.id)
    if search != '':
        users_list = users_list.filter(
            Users.first_name.like('%' + search + '%') | Users.last_name.like('%' + search + '%') | (
                    Users.barcode == search))
    if city != '' and city != 0:
        users_list = users_list.filter_by(city=city)
    if course != '' and course != 0:
        users_list = users_list.filter_by(course=course)
    if edu_program != '' and edu_program != 0:
        users_list = users_list.filter_by(edu_program=edu_program)

    users_list = users_list.paginate(1, 10)

    cities = Cities.get_cities()
    edu_programs = EduPrograms.get_edu_programs()

    return render_template('find-friends.html', user=user, users=users_list, search=search, cities=cities,
                           edu_programs=edu_programs, selected_city=city, selected_course=course,
                           selected_edu_program=edu_program)
