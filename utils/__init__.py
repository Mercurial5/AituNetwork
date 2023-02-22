
from utils.PicturesDB import PicturesDB
from flask import session, redirect, url_for
from email.message import EmailMessage
from smtplib import SMTP_SSL
from random import randint
from os import getenv
import functools

picturesDB = PicturesDB()


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from aituNetwork.models import Users
        if session.get('user') is None:
            return redirect(url_for('auth.login'))

        user = session['user']
        if Users.is_user_correct(user):
            return func(*args, **kwargs)

        del session['user']
        return redirect(url_for('auth.login'))

    return wrapper


def send_email(to: str, token_link: str, header: str, msg: str):
    message = EmailMessage()
    message['Subject'] = header
    message['From'] = getenv('SMTP_SENDER')
    message['To'] = to
    message.set_content(msg % token_link)

    with SMTP_SSL('smtp.gmail.com', int(getenv('SMTP_PORT'))) as smtp:
        smtp.login(getenv('SMTP_SENDER'), getenv('SMTP_PASSWORD'))
        smtp.send_message(message)


def random_id():
    from aituNetwork.models import Users

    mn = 1000000
    mx = 9999999

    rand = randint(mn, mx)
    while Users.query.filter_by(id=rand).first() is not None:
        rand = randint(mn, mx)

    return str(rand)
