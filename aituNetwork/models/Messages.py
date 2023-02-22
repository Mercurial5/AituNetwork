from aituNetwork.models import db
from datetime import datetime

import mongoengine
from bson.objectid import ObjectId

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, index=True)
    message = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, index=True, nullable=False, default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'user_id': self.user_id,
            'message': self.message,
            'created': self.created.__str__()
        }

    @staticmethod
    def get_messages(chat_id: int, offset: int, limit: int):
        messages = Messages.query.filter_by(chat_id=chat_id).order_by(Messages.id.desc()).limit(limit).offset(offset)

        return messages.all()

    @staticmethod
    def get_last_message(chat_id: int):
        return Messages.query.filter_by(chat_id=chat_id).order_by(Messages.id.desc()).first()

    @staticmethod
    def delete_messages_in_chat(chat_id: int):
        Messages.query.filter_by(chat_id=chat_id).delete()


class MessagesCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)
    chat = mongoengine.ReferenceField(document_type="chat")
    user = mongoengine.ReferenceField(document_type="user")
    message = mongoengine.StringField(unique=True, required=True)
    created = mongoengine.DateTimeField(default=datetime.now)

    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat,
            'user_id': self.user,
            'message': self.message,
            'created': self.created.__str__()
        }

    @staticmethod
    def get_messages(chat_id: int, offset: int, limit: int):
        pass

    @staticmethod
    def get_last_message(chat_id: int):
        pass

    @staticmethod
    def delete_messages_in_chat(chat_id: int):
        db.messages.deleteOne({"chat.chat_id": chat_id})