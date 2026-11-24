from functools import wraps

from flask import abort, flash, jsonify, redirect, session, url_for

from models.conn import db
from models.model import User


def get_current_user():
    user_id = session.get('user_id')
    if user_id is None:
        return None
    return db.session.get(User, user_id)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if get_current_user() is None:
            flash('Accedi per continuare', 'warning')
            return redirect(url_for('frontend.login'))
        return view(*args, **kwargs)
    return wrapped



def api_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if get_current_user() is None:
            return jsonify({'error': 'authentication required'}), 401
        return view(*args, **kwargs)
    return wrapped
