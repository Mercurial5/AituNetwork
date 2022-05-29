from aituNetwork.models import Users, ProfilePictures, PostLikes


def get_user(user_id: int):
    return Users.get(user_id)


def is_user_liked(user_id: int, post_id: int):
    if PostLikes.get_post_like(user_id, post_id) is not None:
        return True
    return False


def get_picture(user_id: int):
    return ProfilePictures.get_profile_picture(user_id)