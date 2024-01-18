#!/usr/bin/env python3
"""
handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    handles session login
    """
    email = request.form.get('email')
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user: User = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    # create a session ID for the user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    cookie_name = getenv('SESSION_NAME')
    res.set_cookie(cookie_name, session_id)
    return res


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """
    logs out a user and destroys a session
    """
    from api.v1.app import auth
    session_ended = auth.destroy_session(request)
    if session_ended:
        return jsonify(), 200
    else:
        abort(404)
