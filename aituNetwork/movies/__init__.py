from flask import Blueprint

movies = Blueprint('movies', __name__, template_folder='template', static_folder='static')

from aituNetwork.movies import routes
