from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.product import Product
from models.category import Category
from bcrypt import checkpw


@app_views.route("/products", methods=['GET'], strict_slashes=False)
@app_views.route("/products/<int:product_id>", methods=['GET'], strict_slashes=False)
@app_views.route("/categories/<int:category_id>/products", methods=['GET'], strict_slashes=False)
def yourProducts(category_id: int = None, product_id: int = None):
    """get product data"""
    if category_id:
        ctg = storage.get(Category, category_id)
        if ctg:
            return jsonify({"products": [product.to_dict() for product in ctg.products]}), 200
    elif product_id:
        product = storage.get(Product, product_id)
        if product:
            return jsonify({"product": product.to_dict()}), 200
    else:
        products = storage.all(Product).values()
        return jsonify({"products": [product.to_dict() for product in products]}), 200
    abort(404)


@app_views.route("/categories/<int:category_id>/products", methods=['POST'], strict_slashes=False)
def createProduct(category_id=None):
    """POST product data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    store = request.user.store
    if store:
        ctg = storage.get(Category, category_id)
        if ctg:
            if ctg in store.categories:
                if all(dt in data for dt in ('name', 'price', 'stock', 'images', 'location')):
                    product = Product(
                        name=data['name'],
                        category_id=ctg.id
                    )
                    storage.update(product, **data)
                    return jsonify({"message": "product created successfully"}), 200
                return jsonify({"error": "Name and description is mandatory"}), 400
            return jsonify({"error": "Not Allowed!"}), 400
        return jsonify({"error": "You should have category!, Create One!"}), 400
    return jsonify({"error": "You should have Store!, Create One!"}), 400


@app_views.route("/products/<int:product_id>", methods=['PUT'], strict_slashes=False)
def updateProduct(product_id=None):
    """update product data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"})

    store = request.user.store
    if store:
        product = storage.get(Product, product_id)
        if product:
            ctg = storage.get(Category, product.category_id)
            if ctg in store.categories:
                storage.update(product, **data)
                return jsonify({"message": "Product updated successfully"}), 200
            return jsonify({"error": "Not Allowed!"}), 400
    abort(404)


@app_views.route("/products/<int:product_id>", methods=['DELETE'], strict_slashes=False)
def deleteProduct(product_id: int):
    """delete product"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    store = request.user.store
    if store:
        prd = storage.get(Product, product_id)
        if prd:
            ctg = storage.get(Category, prd.category_id)
            if ctg in store.categories:
                if 'password' in data and checkpw(data['password'].encode(), request.user.password.encode()):
                    for rev in prd.reviews:
                        rev.delete()
                    prd.delete()
                    storage.save()
                    return jsonify({"message": "product deleted successfully"}), 200
                return jsonify({"error": "Your password incorrect"}), 400
            return jsonify({"error": "Category Not Found!"}), 400
        return jsonify({"error": "Product Not Found!"}), 400
    return jsonify({"error": "Store not Found Create One!"}), 400
