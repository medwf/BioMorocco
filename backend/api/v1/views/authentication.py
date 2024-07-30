from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/signUp', methods=['POST'], strict_slashes=False)
def users():
    """create a user with post methods"""
    from api.v1.app import AUTH, Email
    from api.v1.utils.image import upload_image
    import json

    data = request.form.get("data", None)
    # print("*", data, type(data))
    if data:
        try:
            data = json.loads(data)
            # print("**", data, type(data))
        except json.JSONDecodeError:
            # print("**", data, type(data))
            data = None

    # print("***", data, type(data))
    if not data and 'file' not in request.files:
        return jsonify({'error': 'check your data Send!'}), 400

    if data:
        email = data.get('email', None)
        password = data.get('password', None)

        if email and password:
            user = AUTH.register_user(data)
            if user:
                content = Email.signUp(
                    f'{user.first_name} {user.last_name}',
                    email
                )
                upload_image(request, user)
                Email.sendEmail(email, content)
                return jsonify({"message": f'User {user.email} created successfully'}), 201
            return jsonify({'error': 'Email already registered'}), 400
        return jsonify({'error': 'should have email and password'}), 400
    return jsonify({'error': 'check your data send'}), 400


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


@app_views.route('/forget_password', methods=['POST'], strict_slashes=False)
def get_forget_password():
    """Reset password"""
    from api.v1.app import AUTH, Email
    from models import storage

    data = request.get_json(force=True, silent=True)
    if data and 'email' in data:
        user = storage.find_user_by(email=data['email'])
        if user:
            code = AUTH.create_code_for_reset_password(user.id)
            content = Email.create_content_for_forget_Password(
                f"{user.first_name} {user.last_name}", user.email, code
            )
            Email.sendEmail(user.email, content)
            return jsonify({'message': 'Code Sended Successfully'}), 200
        return jsonify({'error': 'User Not Found'}), 404
    return jsonify({'error': 'check your data send'}), 400


@app_views.route('/forget_password', methods=['PUT'], strict_slashes=False)
def put_forget_password():
    """Reset password"""
    from api.v1.app import AUTH
    data = request.get_json(force=True, silent=True)
    if data:
        code = data.get('code', None)
        new_password = data.get('new_password', None)
        confirmed = data.get('confirmed', None)
        if code and confirmed and new_password:
            user = AUTH.check_code_for_reset_password(code)
            if not user:
                return jsonify({'error': 'You code was Expired or not correct!'}), 400
            if new_password == confirmed:
                user.password = new_password
                user.save()
                return jsonify({'message': 'password changed'}), 200
            return jsonify({'error': 'new_password be same as confirmed'}), 400
        return jsonify({'error': 'should have code and password and confirmed and new one'}), 400
    return jsonify({'error': 'check your data send'}), 400


@app_views.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """delete session"""
    from api.v1.app import AUTH

    AUTH.destroy_session()
    return jsonify({'message': 'Logout successful'})
