from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.product import Product
from models.order import Order


@app_views.route("/product/<int:product_id>/orders", methods=['GET'], strict_slashes=False)
@app_views.route("/users/orders", methods=['GET'], strict_slashes=False)
def Orders(product_id=None):
    """get Order data"""
    if product_id:
        product = storage.get(Product, product_id)
        if product:
            return jsonify({"orders": [order.to_dict() for order in product.orders]}), 200
    elif request.user:
        return jsonify({"Orders": [order.to_dict() for order in request.user.orders]}), 200
    abort(404)


@app_views.route("/product/<int:product_id>/orders", methods=['POST'], strict_slashes=False)
@app_views.route("/users/orders", methods=['POST'], strict_slashes=False)
def createOrders(product_id=None):
    """POST order data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    message = []
    error = []

    # selected one product directly
    if product_id:
        product = storage.get(Product, product_id)
        products = [(product, data['quantity'])]

    # selected product from cart.
    elif request.user and request.user.cart:
        products = []
        if 'product_ids' in data:
            # no product found
            if not len(data['product_ids']):
                return jsonify({'error': 'Your cart is Empty!'}), 404

            # selected products
            elif 'product_ids' in data:
                for productId in data['product_ids']:
                    for cartItem in request.user.cart.cartItems:
                        if cartItem.product_id == productId:
                            product = storage.get(Product, cartItem.product_id)
                            products.append((product, cartItem.quantity))

    for (product, quantity) in products:
        if product and product.stock and (product.stock - quantity) > 0:

            order = Order(
                status="pending",
                quantity=quantity,
                total_price=(product.price * quantity) if request.user.country ==
                'Morocco' else (product.price * quantity) + 100,
                orderValid=0,
                user_id=request.user.id,
                product_id=product.id
            )
            storage.update(product, stock=(product.stock - order.quantity))
            storage.new(order)
            storage.save()
            # if product.stock < 10:
            # sending msg to user store tell them he have an order by sending name and phone and address.
            # sending msg tell then that your store product is last then 10.
            message.append(
                f"Order in product id: {product.id}, name: {product.name} created Successfully")
        else:

            # sending msg to user store tell them he have an order but it is not found check your stock.
            error.append(
                f"Order in product id: {product.id}, name: {product.name} Not Found or not enough!"
            )
    return jsonify({"response": {"message": [msg for msg in message], "error": [err for err in error]}}), 200
