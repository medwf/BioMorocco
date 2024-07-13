from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.product import Product
from models.cart import CartItem


@app_views.route("/cartItems", methods=['GET'], strict_slashes=False)
def cartItems():
    """get store data"""
    if request.user and request.user.cart:
        cartItems = request.user.cart.cartItems
        return jsonify({"cartItems": [crtItm.to_dict() for crtItm in cartItems]}), 200
    abort(404)


@app_views.route("/products/<int:product_id>/cartItems", methods=['POST'], strict_slashes=False)
def addCart(product_id):
    """get store data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        quantity = 1

    product = storage.get(Product, product_id)
    if product:
        if request.user and request.user.cart:
            if f"'product_id': {product_id}" in f"{[crtItm.to_dict() for crtItm in request.user.cart.cartItems]}":
                return jsonify({'error': 'you have that product in carts'})
            crtItem = CartItem(
                cart_id=request.user.cart.id,
                product_id=product_id,
                quantity=data['quantity'] if data.get('quantity') else quantity
            )
            crtItem.save()
            return jsonify({"message": "product added successfully"}), 200
    abort(404)


@app_views.route("/cartItems/<int:cartItem_id>", methods=['PUT'], strict_slashes=False)
def updateCart(cartItem_id):
    """delete store"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    if request.user and request.user.cart:
        cartItem = storage.get(CartItem, cartItem_id)
        if cartItem:
            storage.update(cartItem, **data)
            storage.save()
            return jsonify({"message": "cart updated successfully"}), 200
    abort(404)


@app_views.route("/cartItems/<int:cartItem_id>", methods=['DELETE'], strict_slashes=False)
def deleteCart(cartItem_id):
    """delete store"""
    if request.user and request.user.cart:
        cartItem = storage.get(CartItem, cartItem_id)
        if cartItem:
            cartItem.delete()
            storage.save()
            return jsonify({"message": "cart deleted successfully"}), 200
    abort(404)
