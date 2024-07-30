from flask import jsonify, request
from api.v1.views import app_views
from bcrypt import checkpw


@app_views.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """get profile based on session id"""
    return jsonify({
        'user': request.user.to_dict(),
        'cartItems': [item.to_dict() for item in request.user.cartItems],
        'address': [add.to_dict() for add in request.user.addresses],
        'wishlists': [wish.to_dict() for wish in request.user.wishlists],
        'searches': [srx.to_dict() for srx in request.user.searches]
    }), 200


@app_views.route('/users', methods=['PUT'], strict_slashes=False)
def UpdateUser():
    """delete session"""
    import json
    from models import storage
    from api.v1.utils.image import upload_image
    data = request.form.get("data", None)
    if data:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = None

    if not data and 'file' not in request.files:
        return jsonify({'error': 'check your data Send!'}), 400

    if data:
        storage.update(request.user, **data)
    upload_image(request, request.user)
    return jsonify({'message': 'Your Information updated!'}), 200


@app_views.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """Reset password"""
    data = request.get_json(force=True, silent=True)
    if data:
        password = data.get('password', None)
        new_password = data.get('new_password', None)
        confirmed = data.get('confirmed', None)
        if password and confirmed and new_password:
            if checkpw(password.encode(), request.user.password.encode()):
                if new_password == confirmed:
                    request.user.password = new_password
                    request.user.save()
                    return jsonify({'message': 'password changed'}), 200
                return jsonify({'error': 'new_password should be same as confirmed'}), 400
            return jsonify({'error': 'password not correct'}), 400
        return jsonify({'error': 'should have password and confirmed and new one'}), 400
    return jsonify({'error': 'check your data send'}), 400


@app_views.route('/users', methods=['DELETE'], strict_slashes=False)
def deleteUser():
    """delete session"""
    from api.v1.app import AUTH
    from models import storage
    from api.v1.utils.image import deleted_image

    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    if 'password' in data and checkpw(data['password'].encode(), request.user.password.encode()):
        store = request.user.store
        if store:
            for prd in store.products:
                deleted_image(request.method, prd)
            deleted_image(request.method, store)

        deleted_image(request.method, request.user)
        AUTH.destroy_session()
        storage.delete(request.user)
        storage.save()
        return jsonify({'message': 'Your account was deleted!'}), 200
    return jsonify({"error": "Your password incorrect"}), 400
