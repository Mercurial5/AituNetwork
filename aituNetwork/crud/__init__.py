from flask import Blueprint

crud = Blueprint('crud', __name__)

from aituNetwork.crud import routes
