#!/usr/bin/env python3
"""
This module performs an end to end integration test of the
authentication service
"""
import requests
base_url = "http://localhost:5000"


def register_user(email: str, password: str):
    """
    test registering a new user
    """
    data = {
        'email': email,
        'password': password
    }
    url = "{}/users".format(base_url)
    res = requests.post(url, data=data)
    res_json = res.json()
    assert res_json == {"email": "{}".format(email), "message": "user created"}
    assert res.status_code == 200


def log_in_wrong_password(email: str, password: str):
    """
    tests logging in with invalid password
    """
    data = {
        'email': email,
        'password': password
    }
    url = "{}/sessions".format(base_url)
    res = requests.post(url, data=data)
    assert res.status_code == 401


def profile_unlogged():
    """
    test accessing profile for an unauthenticated user
    """
    url = "{}/profile".format(base_url)
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str):
    """
    test accessing profile for a logged in user
    """
    url = "{}/profile".format(base_url)
    cookies = {
        'session_id': session_id
    }
    res = requests.get(url, cookies=cookies)
    res_json = res.json()
    assert res.status_code == 200
    assert 'email' in res_json


def log_in(email: str, password: str):
    """
    test log in
    """
    data = {
        'email': email,
        'password': password
    }
    url = "{}/sessions".format(base_url)
    res = requests.post(url, data=data)
    res_json = res.json()
    session_id = res.cookies.get('session_id')
    assert res.status_code == 200
    assert res_json == ({"email": email, "message": "logged in"})
    assert session_id is not None
    return session_id


def log_out(session_id):
    """
    test logout function
    """
    url = "{}/sessions".format(base_url)
    cookies = {
        'session_id': session_id
    }
    res = requests.delete(url, cookies=cookies)
    assert res.status_code == 200


def reset_password_token(email: str):
    """
    test reset_password token generation
    """
    url = "{}/reset_password".format(base_url)
    data = {
        'email': email
    }
    res = requests.post(url, data=data)
    res_json = res.json()
    reset_token = res_json.get('reset_token')
    assert res.status_code == 200
    assert res_json == {"email": email, "reset_token": reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str):
    """
    test updating password
    """
    url = "{}/reset_password".format(base_url)
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    res = requests.put(url, data=data)
    res_json = res.json()
    assert res.status_code == 200
    assert res_json == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
