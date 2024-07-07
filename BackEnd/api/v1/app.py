#!/usr/bin/env python3
"""
Main module For The Flask Web Application
"""
# from models import storage
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

AUTH = SessionDBAuth()


@app.before_request
def beforeRequest() -> str:
    """handle auth before request"""
    if AUTH.require_auth(request.path, [
            '/api/v1/',
            '/api/v1/stat*',
            '/api/v1/signUp/',
            '/api/v1/login/'
    ]):
        if AUTH.session_cookie(request) is None:
            abort(401)
        request.user = AUTH.current_user(request)
        if request.user is None:
            abort(403)


@app.teardown_appcontext
def close(CXT):
    """Close the database session after each request."""
    from models import storage
    storage.close()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def un_authorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == '__main__':
    HOST = getenv('API_HOST', '0.0.0.0')
    PORT = getenv('API_PORT', '5000')
    app.run(host=HOST, port=PORT, debug=True)
