from aituNetwork.models import db
from datetime import datetime

import mongoengine
from bson.objectid import ObjectId


class SeenMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    message_id = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.DATETIME, default=datetime.now)

    @staticmethod
    def count_of_messages_of_user(user_id: int):
        return SeenMessages.query.filter_by(user_id=user_id).with_entities(SeenMessages.message_id)

    @staticmethod
    def update(new_messages: list):
        db.session.add_all(new_messages)
        db.session.commit()


class SeenMessagesCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)
    user_id = mongoengine.ReferenceField(document_type="user")
    message_id = mongoengine.ReferenceField(document_type="message")
    date = mongoengine.DateTimeField(default=datetime.now)

    @staticmethod
    def count_of_messages_of_user(user_id: int):
        pass

    @staticmethod
    def update(new_messages: list):
        pass