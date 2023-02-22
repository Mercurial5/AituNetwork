from aituNetwork.models import db
from datetime import datetime

import mongoengine
from bson.objectid import ObjectId

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, nullable=False, default=datetime.now)

    @staticmethod
    def get(comment_id: int):
        return Comments.query.get(comment_id)

    @staticmethod
    def create_comment(user_id: int, text: str):
        comment = Comments(user_id=user_id, text=text)
        db.session.add(comment)
        db.session.commit()

        return comment

    @staticmethod
    def delete_comment(comment_id: int):
        Comments.query.filter_by(id=comment_id).delete()
        db.session.commit()

    @staticmethod
    def delete_for_deleted_user(user_id: int):
        comments_id_list = Comments.query.filter_by(user_id=user_id).with_entities(Comments.id).all()

        Comments.query.filter_by(user_id=user_id).delete()

        return comments_id_list


class CommentsCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)
    user = mongoengine.ReferenceField(document_type="Users")
    text = mongoengine.StringField(unique=True, required=True)
    created = mongoengine.DateTimeField(default=datetime.now)

    @staticmethod
    def get(comment_id: int):
        return db.comments.find({"id": comment_id})

    @staticmethod
    def create_comment(user_id: int, text: str):
        comment = db.comments.insertOne({"user_id": user_id, "text": text})

        return comment

    @staticmethod
    def delete_comment(comment_id: int):
        db.commets.deleteOne({"id": comment_id})

    @staticmethod
    def delete_for_deleted_user(user_id: int):
        pass