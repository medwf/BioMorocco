#!/usr/bin/env python3
"""
Main module For The Flask Web Application
"""
from os import getenv, getcwd
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask import Flask, jsonify, request, abort, send_from_directory
from api.v1.views import app_views
from api.v1.utils.session_db_auth import SessionDBAuth
from api.v1.utils.db_redis import RedisClient
from api.v1.utils.sendEmail import SendEmail


# URL for exposing Swagger UI (without trailing '/')
SWAGGER_URL = '/api/v1/docs'
API_URL = '/api/v1/static/swagger.json'


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}},
     supports_credentials=True)

Email = SendEmail()
AUTH = SessionDBAuth()
redis_client = RedisClient()


# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


@app.before_request
def beforeRequest() -> str:
    """handle auth before request"""
    print(request.path)
    # print(request.method)
    if AUTH.require_auth(request.method, request.path, [
            '/api/v1/',
            '/api/v1/stat*',
            '/api/v1/signUp/',
            '/api/v1/login/',
            '/api/v1/forget_password/',
            '/api/v1/docs*'
    ]):
        if AUTH.session_cookie(request) is None:
            abort(401)
        request.user = AUTH.current_user(request)
        if request.user is None:
            abort(403)


@app.route("/api/v1/static/swagger.json")
def specs():
    return send_from_directory(getcwd(), "api/v1/static/swagger.json")


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
