from aituNetwork.models import db
from datetime import datetime


class SeenMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    message_id = db.Column(db.Integer, index=True, nullable=False)
    date = db.Column(db.DATETIME, default=datetime.now)
