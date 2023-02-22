from aituNetwork.models import db
from datetime import datetime

import mongoengine
from bson.objectid import ObjectId


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)

    @staticmethod
    def is_admin(user_id: int):
        return Admins.query.filter_by(user_id=user_id).first() is not None


class AdminsCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)
    user = mongoengine.ReferenceField("Users")

    @staticmethod
    def is_admin(user_id: int):
        return db.user.findOne({"user_id": user_id}) is not None
