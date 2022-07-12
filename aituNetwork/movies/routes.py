from flask import request, render_template, session
from aituNetwork.movies import movies
from utils import auth_required
import requests


headers = {'X-API-KEY': '1af58e0d-6f44-4ec0-9a57-5a51c892f857', 'Content-Type': 'application/json'}


@movies.route('/')
@auth_required
def movie_list():
    search_text = request.values.get('search-text')

    url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/'
    if search_text:
        url += 'search-by-keyword'
        params = {'keyword': search_text}
    else:
        url += 'top'
        params = {'type': 'TOP_100_POPULAR_FILMS'}

    response = requests.get(url, params=params, headers=headers).json()
    return render_template('movies.html', user=session['user'], films=response['films'], search_text=search_text)


@movies.route('/<film_id>')
@auth_required
def movie(film_id):
    api_url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/' + film_id

    response = requests.get(api_url, headers=headers, params={'id': film_id}).json()
    return render_template('movie_player.html', user=session['user'], film=response['data'])
