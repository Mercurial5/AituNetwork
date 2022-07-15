from aituNetwork.models import db
from datetime import datetime


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
