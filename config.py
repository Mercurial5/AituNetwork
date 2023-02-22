from dotenv import load_dotenv
from os import getenv

from urllib.parse import quote_plus

load_dotenv()

db = {
    'user': getenv('DATABASE_USER'),
    'password': getenv('DATABASE_PASSWORD'),
    'host': getenv('DATABASE_HOST'),
    'name': getenv('DATABASE_NAME')
}

atlas_db = {
    'user': getenv('ATLAS_DB_USER'),
    'password': getenv('ATLAS_DB_PASSWORD'),
    'cluster': getenv('ATLAS_DB_CLUSTER')
}


class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db["user"]}:{quote_plus(db["password"])}@{db["host"]}/{db["name"]}?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY')
    SESSION_TYPE = 'sqlalchemy'
    ATLAS_DATABASE_LINK = f'mongodb+srv://{atlas_db["user"]}:{atlas_db["password"]}@{atlas_db["cluster"]}.xdkdjnk.mongodb.net/?retryWrites=true&w=majority'
