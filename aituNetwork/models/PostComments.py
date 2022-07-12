from aituNetwork.models import db


class PostComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False, index=True)
    comment_id = db.Column(db.Integer, nullable=False, index=True)

    @staticmethod
    def get(post_id: int):
        return PostComments.query.filter_by(post_id=post_id).all()

    @staticmethod
    def add_comment_to_post(post_id: int, comment_id: int):
        post_comment = PostComments(post_id=post_id, comment_id=comment_id)
        db.session.add(post_comment)
        db.session.commit()

    @staticmethod
    def delete_comment_from_post(comment_id: int):
        PostComments.query.filter_by(comment_id=comment_id).delete()
        db.session.commit()

    @staticmethod
    def delete_comments_from_post(post_id: int):
        PostComments.query.filter_by(post_id=post_id).delete()
        db.session.commit()
