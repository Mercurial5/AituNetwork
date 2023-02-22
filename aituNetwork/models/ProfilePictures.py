from aituNetwork.models import db
from datetime import datetime

import mongoengine
from bson.objectid import ObjectId

class ProfilePictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    added = db.Column(db.DATETIME, nullable=False, default=datetime.now)

    @staticmethod
    def get_profile_picture(user_id: int):
        return ProfilePictures.query.filter_by(user_id=user_id).order_by(ProfilePictures.id.desc()).first()

    @staticmethod
    def delete_pictures_for_deleted_user(user_id: int):
        pictures = ProfilePictures.query.filter_by(user_id=user_id).all()

        ProfilePictures.query.filter_by(user_id=user_id).delete()

        return pictures


class ProfilePicturesCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)
    user_id = mongoengine.ReferenceField(document_type="user")
    name = mongoengine.StringField(unique=True, max_length=255, required=True)
    extension = mongoengine.StringField(max_length=255, required=True)
    added = mongoengine.DateTimeField(default=datetime.now, required=True)

    @staticmethod
    def get_profile_picture(user_id: int):
        return ProfilePictures.query.filter_by(user_id=user_id).order_by(ProfilePictures.id.desc()).first()

    @staticmethod
    def delete_pictures_for_deleted_user(user_id: int):
        pictures = ProfilePictures.query.filter_by(user_id=user_id).all()

        ProfilePictures.query.filter_by(user_id=user_id).delete()

        return pictures