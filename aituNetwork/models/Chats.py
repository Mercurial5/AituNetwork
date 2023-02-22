from aituNetwork.models import db

import mongoengine
from bson.objectid import ObjectId


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def get(chat_id: int):
        return Chats.query.get(chat_id)

    @staticmethod
    def is_chat_exist(chat_id: int) -> bool:
        return Chats.query.get(chat_id) is not None

    @staticmethod
    def create_chat() -> int:
        chat = Chats()
        db.session.add(chat)
        db.session.commit()

        return chat.id

    @staticmethod
    def delete_chat(chat_id: int):
        Chats.query.filter_by(id=chat_id).delete()


class ChatsCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)

    @staticmethod
    def get(chat_id: int):
        return db.chats.findOne({"chat_id": chat_id})

    @staticmethod
    def is_chat_exist(chat_id: int) -> bool:
        return db.chats.findOne({"chat_id": chat_id}) is not None

    @staticmethod
    def create_chat() -> int:
        inserted = db.chats.InsertOne({"id": id})

        return inserted.id

    @staticmethod
    def delete_chat(chat_id: int):
        db.chats.deleteOne({"id": chat_id})
