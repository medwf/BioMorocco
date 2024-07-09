#!/usr/bin/env python3
""" Module of Index Views """

from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.user import User
from models.order import Order
from models.review import Review
from models.product import Product
from models.category import Category
from models.store import Store


@app_views.route("/", strict_slashes=False, methods=["GET"])
def Hello():
    """ Say Hello"""
    return make_response(jsonify({'message': 'You are Welcome'}), 200)


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """return status ok, 200"""
    response_data = {
        "app_name": "Bio Morocco Products",
        "version": "1.0",
        "description": "Bio Morocco Products Reset Full API",
        "year_founded": 2024,
        "country": "Morocco",
        "status": "OK",
    }
    return make_response(jsonify(response_data), 200)


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    """return json list count all tables"""
    # from models import storage

    Stores = storage.count(Store)
    categories = storage.count(Category)
    products = storage.count(Product)
    users = storage.count(User)
    projects = storage.count(Order)
    reviews = storage.count(Review)
    return make_response(jsonify({
        "store": Stores,
        "category": categories,
        "product": products,
        "users": users,
        "projects": projects,
        "reviews": reviews
    }), 200)
