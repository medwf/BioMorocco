from flask import jsonify, make_response, request, abort, redirect
from api.v1.views import app_views
from bcrypt import checkpw


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
                    response = jsonify(
                        {'email': email, 'message': 'logged in'})
                    response.set_cookie('session_id', session_id)
                    return response
        return jsonify({'email': email, 'message': 'check your email and password!'})
    return jsonify({'message': 'check your data send'})


@app_views.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """delete session"""
    from api.v1.app import AUTH

    AUTH.destroy_session(request.user)
    return redirect('/api/v1/')


@app_views.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """get profile based on session id"""
    return jsonify({
        'user': request.user.to_dict(),
        'cart': request.user.cart.to_dict(),
        'cartItems': [item.to_dict() for item in request.user.cart.cartItems]
    }), 200


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
                return jsonify({'email': email, 'message': 'user created'}), 200
            return jsonify({'message': 'email already registered'}), 400
        return jsonify({'message': 'should have email and password'})
    return jsonify({'message': 'check your data send'})


@app_views.route('/users', methods=['PUT'], strict_slashes=False)
def UpdateUser():
    """delete session"""
    from models import storage
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'message': 'check your data send'})

    storage.update_user(request.user, **data)
    return jsonify({'message': 'Your Information updated!'})


@app_views.route('/users', methods=['DELETE'], strict_slashes=False)
def deleteUser():
    """delete session"""
    from api.v1.app import AUTH
    from models import storage

    AUTH.destroy_session(request.user)
    cart = request.user.cart
    for cartItem in cart.cartItems:
        cartItem.delete()
    cart.delete()
    request.user.delete()
    storage.save()
    return jsonify({'message': 'Your account was deleted!'})


@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """Reset password"""
    data = request.get_json(force=True, silent=True)
    if data:
        password = data.get('password', None)
        confirmed_password = data.get('confirmed_password', None)
        new_password = data.get('new_password', None)
        if password and confirmed_password and new_password:
            if password == confirmed_password:
                if checkpw(password.encode(), request.user.password.encode()):
                    request.user.password = new_password
                    request.user.save()
                    return jsonify({'message': 'password changed'})
                return jsonify({'message': 'password not correct'})
            return jsonify({'message': 'password be same as confirmed'})
        return jsonify({'message': 'should have password and confirmed and new one'})
    return jsonify({'message': 'check your data send'})
