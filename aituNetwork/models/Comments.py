from aituNetwork.models import db
from datetime import datetime


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, nullable=False, default=datetime.now)
