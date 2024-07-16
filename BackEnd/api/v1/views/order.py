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
    from api.v1.app import Email
    from models.category import Category
    from models.store import Store
    from models.user import User
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    message = []
    error = []

    # selected one product directly
    if product_id:
        product = storage.get(Product, product_id)
        quantity = data['quantity']
        total_price = (product.price * quantity) if request.user.country == 'Morocco' else (
            product.price * quantity) + 100
        products = [(product, quantity, total_price)]

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
                            quantity = cartItem.quantity
                            total_price = (product.price * quantity) if request.user.country == 'Morocco' else (
                                product.price * quantity) + 100
                            products.append((product, quantity, total_price))

    for (product, quantity, total_price) in products:
        if product and product.stock and (product.stock - quantity) > 0:

            order = Order(
                status="pending",
                quantity=quantity,
                total_price=total_price,
                orderValid=0,
                user_id=request.user.id,
                product_id=product.id
            )
            storage.update(product, stock=(product.stock - order.quantity))
            storage.new(order)
            storage.save()
            category = storage.get(Category, product.category_id)
            store = storage.get(Store, category.store_id)
            owner = storage.get(User, store.user_id)

            # sending msg tell then that your store product is last then 10.
            if product.stock < product.declare_stock:
                content = Email.create_content_for_low_stock_dedicated(
                    owner, product
                )
                Email.sendEmail(owner.email, content)

            message.append(
                f"Order in product id: {product.id}, name: {product.name} created Successfully")
        else:

            # sending msg to user store tell them he have an order but it is not found check your stock.
            error.append(
                f"Order in product id: {product.id}, name: {product.name} Not Found or not enough!"
            )
    # sending msg to user store tell them he have an order by sending name and phone and address.
    content = Email.create_content_for_new_order(
        owner, products, request.user
    )
    Email.sendEmail(owner.email, content)
    return jsonify({"response": {"message": [msg for msg in message], "error": [err for err in error]}}), 200
