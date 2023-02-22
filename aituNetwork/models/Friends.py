from aituNetwork.models import db

import mongoengine
from bson.objectid import ObjectId

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    friend_id = db.Column(db.Integer, index=True, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id'),)

    @staticmethod
    def add_friend(user_id: int, friend_id: int):
        if Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first() is None:
            friend = Friends(user_id=user_id, friend_id=friend_id)
            db.session.add(friend)
            db.session.commit()

    @staticmethod
    def remove_friend(user_id: int, friend_id: int):
        if Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first() is not None:
            Friends.query.filter_by(user_id=user_id, friend_id=friend_id).delete()
            db.session.commit()

    @staticmethod
    def get_friend_list(user_id: int, only_query: bool = False):
        query = Friends.query.filter(
            Friends.user_id.in_(
                Friends.query.filter_by(user_id=user_id).with_entities(Friends.friend_id)
            ),
            Friends.friend_id == user_id
        )

        if only_query:
            return query

        return query.all()

    @staticmethod
    def get_friend_status(user_id: int, friend_id: int) -> int:
        is_my_friend = Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        am_i_friend = Friends.query.filter_by(user_id=friend_id, friend_id=user_id).first()

        # friend_status
        # 1: I sent request
        # 2: Profile user sent request
        # 3: Friends

        friend_status = None
        if is_my_friend is not None and am_i_friend is not None:
            friend_status = 3
        elif is_my_friend is not None:
            friend_status = 1
        elif am_i_friend is not None:
            friend_status = 2

        return friend_status

    @staticmethod
    def is_friend(user_id: int, friend_id: int):
        return Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first() is not None

    @staticmethod
    def delete_friends_for_deleted_user(user_id: int):
        Friends.query.filter((Friends.user_id == user_id) | (Friends.friend_id == user_id)).delete()


class FriendsCopy(mongoengine.Document):
    id = mongoengine.ObjectIdField(primary_key=True, default=ObjectId)
    user = mongoengine.ReferenceField("Users")
    friend = mongoengine.ReferenceField("Friends", unique_with="user")
    # __table_args__ = (mongoengine.UniqueConstraint('user_id', 'friend_id'),)

    @staticmethod
    def add_friend(user_id: int, friend_id: int):
        if db.friends.find({"user.user_id": user_id, "friend.friend_id": friend_id}) is not None:
            db.friends.insertOne({"user_id": user_id, "friend_id": friend_id})

    @staticmethod
    def remove_friend(user_id: int, friend_id: int):
        if db.friends.find({"user.user_id": user_id, "friend.friend_id": friend_id}) is not None:
            db.friends.deleteOne({"user.user_id": user_id, "friend_id": friend_id})

    @staticmethod
    def get_friend_list(user_id: int, only_query: bool = False):
        pass

    @staticmethod
    def get_friend_status(user_id: int, friend_id: int) -> int:
        is_my_friend = db.friends.find({"user.user_id": user_id, "friend.friend_id": friend_id})
        am_i_friend = db.friends.find({"user.user_id": friend_id, "friend.friend_id": user_id})

        friend_status = None
        if is_my_friend is not None and am_i_friend is not None:
            friend_status = 3
        elif is_my_friend is not None:
            friend_status = 1
        elif am_i_friend is not None:
            friend_status = 2

        return friend_status

    @staticmethod
    def is_friend(user_id: int, friend_id: int):
        return db.friends.find({"user.user_id": user_id, "friend.friend_id": friend_id})

    @staticmethod
    def delete_friends_for_deleted_user(user_id: int):
        pass
