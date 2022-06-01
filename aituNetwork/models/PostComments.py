from aituNetwork.models import db


class PostComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False, index=True)
    comment_id = db.Column(db.Integer, nullable=False, index=True)

    @staticmethod
    def get(post_id: int):
        return PostComments.query.filter_by(post_id=post_id).all()
