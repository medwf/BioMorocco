from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.category import Category
from bcrypt import checkpw


@app_views.route("/categories", methods=['GET'], strict_slashes=False)
@app_views.route("/categories/<int:category_id>", methods=['GET'], strict_slashes=False)
def yourCategories(category_id=None):
    """get category data"""
    if category_id:
        category = storage.get(Category, category_id)
        if category:
            return jsonify({"category": category.to_dict()}), 200
        else:
            return jsonify({"error": "Not Found!"}), 400
    categories = storage.all(Category).values()
    return jsonify({"categories": [category.to_dict() for category in categories]}), 200


@app_views.route("/categories", methods=['POST'], strict_slashes=False)
def createCategory():
    """POST category data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"})

    store = request.user.store
    if store:
        if 'name' in data and 'description' in data:
            category = Category(
                name=data['name'],
                store_id=store.id
            )
            storage.update(category, **data)
            return jsonify({"message": "Category created successfully"}), 200
        return jsonify({"error": "Name and description is mandatory"}), 400
    return jsonify({"error": "You should have Store!, Create One!"}), 400


@app_views.route("/categories/<int:category_id>", methods=['PUT'], strict_slashes=False)
def updateCategory(category_id: int):
    """update category data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"})

    store = request.user.store
    if store:
        category = storage.get(Category, category_id)
        if category:
            storage.update(category, **data)
            return jsonify({"message": "Category updated successfully"}), 200
        abort(404)
    return jsonify({"error": "You should have Store, Create One!"}), 400


@app_views.route("/categories/<int:category_id>", methods=['DELETE'], strict_slashes=False)
def deleteCategory(category_id: int):
    """delete category"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    store = request.user.store
    if store:
        if 'password' in data and checkpw(data['password'].encode(), request.user.password.encode()):
            ctg = storage.get(Category, category_id)
            if ctg:
                for prd in ctg.products:
                    for rev in prd.reviews:
                        rev.delete()
                    prd.delete()
                ctg.delete()
                storage.save()
                return jsonify({"message": "Category deleted successfully"}), 200
            abort(404)
        return jsonify({"error": "Your password incorrect"}), 400
    return jsonify({"error": "Not category found create one!"}), 400
