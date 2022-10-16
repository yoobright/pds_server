from db import db
from db import models


def add_user(values):
    user = models.User()
    user.update(values)
    db.session.add(user)
    db.session.commit()

    return user


def get_all_users(values):
    query = db.session.query(models.User)
    if values.user_name:
        query = query.filter(models.User.user_name == values.user_name)

    users = query.all()

    return users


def get_user_by_id(uid):
    user = db.session.query(models.User).\
        filter(models.User.id == uid).one_or_none()

    return user


def delete_user_by_id(uid):
    res = db.session.query(models.User).\
        filter(models.User.id == uid).delete()
    db.session.commit()

    return res


def update_user_by_id(uid, values):
    user = db.session.query(models.User).\
        filter(models.User.id == uid).one_or_none()

    if user is not None:
        user.update(values)
        db.session.commit()

    return user

