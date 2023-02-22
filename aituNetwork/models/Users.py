from aituNetwork.models import db
from datetime import datetime
from utils import random_id, picturesDB

import mongoengine
from bson.objectid import ObjectId


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, default=random_id)
    barcode = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    about_me = db.Column(db.String(255), nullable=False, default='Hi there! I\'m using AITU Network!')
    birthday = db.Column(db.DATE, nullable=True, index=True)
    city = db.Column(db.Integer, nullable=True, index=True)
    course = db.Column(db.Integer, nullable=True, index=True)
    edu_program = db.Column(db.Integer, nullable=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    registered = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    is_activated = db.Column(db.Boolean, nullable=False, default=False)
    last_online = db.Column(db.String(255), nullable=False, default=datetime.now)

    @staticmethod
    def get(user_id: int):
        return Users.query.get(user_id)

    @staticmethod
    def is_slug_taken(slug: str) -> bool:
        return Users.query.filter_by(slug=slug).first() is not None

    @staticmethod
    def update_user_info(user_id: int, update_info: dict):
        User.objects(id=user_id).first().update(**update_info).save()
        Users.query.filter_by(id=user_id).update(update_info)
        db.session.commit()

    @staticmethod
    def update_user_info_by_barcode(barcode: int, update_info: dict):
        Users.query.filter_by(barcode=barcode).update(update_info)
        db.session.commit()

    @staticmethod
    def get_users_for_new_friends_list(user_id: int):
        return Users.query.filter(Users.is_activated == 1, Users.id != user_id)

    @staticmethod
    def delete_user(user_id: int):
        user = Users.get(user_id)
        db.session.delete(user)

    @staticmethod
    def is_user_correct(user):
        check_user = Users.query.get(user.id)

        if check_user is None:
            return False

        for attr in ['slug', 'password']:
            if getattr(check_user, attr) != getattr(user, attr):
                return False

        return True


class User(mongoengine.Document):
    id = mongoengine.IntField(primary_key=True)
    slug = mongoengine.StringField(unique=True, max_length=255, required=True, default=random_id)
    barcode = mongoengine.IntField(unique=True, required=True)
    first_name = mongoengine.StringField(null=True, max_length=255)
    last_name = mongoengine.StringField(null=True, max_length=255)
    about_me = mongoengine.StringField(null=True, max_length=255,
                                       default='Hi there! I\'m using AITU Network!')
    birthday = mongoengine.DateTimeField(default=datetime.now)
    city = mongoengine.IntField(null=True)
    course = mongoengine.IntField(null=True)
    edu_program = mongoengine.IntField(null=True)
    password = mongoengine.StringField(null=True)
    registered = mongoengine.DateTimeField(default=datetime.now)
    is_activated = mongoengine.BooleanField()
    last_online = mongoengine.DateTimeField(default=datetime.now)

    @staticmethod
    def get(user_id: int):
        pass

    @staticmethod
    def is_slug_taken(slug: str) -> bool:
        pass

    @staticmethod
    def update_user_info(user_id: int, update_info: dict):
        pass

    @staticmethod
    def update_user_info_by_barcode(barcode: int, update_info: dict):
        pass

    @staticmethod
    def get_users_for_new_friends_list(user_id: int):
        pass

    @staticmethod
    def delete_user(user_id: int):
        pass

    @staticmethod
    def is_user_correct(user):
        pass
