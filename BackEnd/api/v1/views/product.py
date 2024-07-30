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
    from api.v1.utils.image import upload_image
    import json

    data = request.form.get("data", None)
    if data:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = None

    if not data and 'file' not in request.files:
        return jsonify({'error': 'check your data Send!'}), 400

    store = request.user.store
    if store:
        ctg = storage.get(Category, category_id)
        if all(dt in data for dt in ('name', 'price', 'stock', 'location')):
            product = Product(
                name=data['name'],
                images="{}",
                category_id=ctg.id if ctg else 0,
                store_id=store.id
            )
            storage.update(product, **data)
            upload_image(request, product)
            return jsonify({"message": "Product Created Successfully"}), 200
        return jsonify({"error": "Name, description, price, images, stock is mandatory"}), 400
    return jsonify({"error": "You should have Store!, Create One!"}), 400


@app_views.route("/products/<int:product_id>", methods=['PUT'], strict_slashes=False)
def updateProduct(product_id=None):
    """update product data"""
    from api.v1.utils.image import upload_image
    import json

    data = request.form.get("data", None)
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        data = None

    if not data and 'file' not in request.files:
        return jsonify({'error': 'check your data Send!'}), 400

    store = request.user.store
    product = storage.get(Product, product_id)
    if store and product and product in store.products:
        if data:
            storage.update(product, **data)
        upload_image(request, product)
        return jsonify({"message": "Product updated successfully"}), 200
    abort(404)


@app_views.route("/products/<int:product_id>", methods=['DELETE'], strict_slashes=False)
def deleteProduct(product_id: int):
    """delete product"""
    from api.v1.utils.image import deleted_image
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    store = request.user.store
    if store:
        prd = storage.get(Product, product_id)
        if prd and prd in store.products:
            if 'password' in data and checkpw(data['password'].encode(), request.user.password.encode()):
                prd.delete()
                storage.save()
                return jsonify({"message": "product deleted successfully"}), 200
            return jsonify({"error": "Your password incorrect"}), 400
        return jsonify({"error": "Product Not Found!"}), 404
    return jsonify({"error": "Store Not Found Create One!"}), 400
