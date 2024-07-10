from flask import jsonify, make_response, request, abort, redirect
from api.v1.views import app_views


@app_views.route('/signUp', methods=['POST'], strict_slashes=False)
def users():
    """create a user with post methods"""
    from api.v1.app import AUTH

    data = request.get_json(force=True, silent=True)
    if data:
        email = data.get('email', None)
        password = data.get('password', None)

        if email and password:
            if AUTH.register_user(data):
                return jsonify({'email': email, 'message': 'user created'}), 201
            return jsonify({'message': 'Email already registered'}), 400
        return jsonify({'message': 'should have email and password'}), 400
    return jsonify({'message': 'check your data send'}), 400


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def session():
    """create session post module"""
    from api.v1.app import AUTH
    data = request.get_json(force=True, silent=True)
    if data:
        email = data.get('email', None)
        password = data.get('password', None)
        # print(email, password)
        if email and password:
            user = AUTH.valid_login(email, password)
            # print("i am here", user)
            if user:
                # print("/login", user.to_dict())
                session_id = AUTH.create_session(user)
                if session_id:
                    response = jsonify({'message': 'Login successful'})
                    response.set_cookie('session_id', session_id)
                    return response
        return jsonify({'error': 'Invalid email or password'}), 400
    return jsonify({'error': 'check your data send'}), 400


@app_views.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """delete session"""
    from api.v1.app import AUTH

    AUTH.destroy_session(request.user)
    return jsonify({'message': 'Logout successful'})
