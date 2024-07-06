from flask import jsonify, make_response, request, abort, redirect
from api.v1.views import app_views


@app_views.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """get profile based on session id"""
    # from api.v1.app import AUTH

    # session_id = request.cookies.get('session_id', None)
    # if session_id:
    #     user = AUTH.get_user_from_session_id(session_id)
    # if user:
    return jsonify({'user': request.current_user.to_dict()}), 200
    # abort(403)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """create a user with post methods"""
    from api.v1.app import AUTH

    email = request.form.get('email', None)
    password = request.form.get('password', None)
    # print(email, password)
    if email and password:
        try:
            AUTH.register_user(email, password)
        except ValueError:
            return jsonify({'message': 'email already registered'}), 400
        return jsonify({'email': email, 'message': 'user created'}), 200
    return jsonify({'message': 'should have email and password'})


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def session():
    """create session post module"""
    from api.v1.app import AUTH

    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email and password:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            if session_id:
                response = jsonify({'email': email, 'message': 'logged in'})
                response.set_cookie('session_id', session_id)
                return response
        return jsonify({'email': email, 'message': 'check your email and password!'})
    abort(401)


@app_views.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """delete session"""
    from api.v1.app import AUTH

    # session_id = request.cookies.get('session_id', None)
    # if session_id:
    #     user = AUTH.get_user_from_session_id(session_id)
    # if user:
    # if request.current_user:
    AUTH.destroy_session(request.current_user.id)
    return redirect('/api/v1/')
    # abort(403)


@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
def genTokenTo_reset_password():
    """Reset password"""
    from api.v1.app import AUTH

    email = request.form.get('email', None)
    if email:
        try:
            token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": token}), 200
        except ValueError:
            pass
    abort(403)


@app_views.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """reset password"""
    from api.v1.app import AUTH

    email = request.form.get('email', None)
    reset_token = request.form.get('reset_token', None)
    new_password = request.form.get('new_password', None)
    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify(
                {'email': email, 'message': 'Password updated'}
            ), 200
        except ValueError:
            pass
    abort(403)
