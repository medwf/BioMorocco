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

    # selected one product directly
    if product_id:
        product = storage.get(Product, product_id)
        if not product:
            return jsonify({'error': f'Product id={product_id} Not Found!'}), 404
        quantity = data['quantity']
        total_price = (product.price * quantity) if request.user.country == 'Morocco' else (
            product.price * quantity) + 100
        products = [(product, quantity, total_price)]

    elif 'product_ids' in data:
        products = []
        if not len(data['product_ids']):
            return jsonify({'error': 'Your cart is Empty!'}), 404

        for productId in data['product_ids']:
            for cartItem in request.user.cart.cartItems:
                if cartItem.product_id == productId:
                    product = storage.get(Product, cartItem.product_id)
                    if not product:
                        return jsonify({'error': 'Product Not Found!'}), 404

                    quantity = cartItem.quantity
                    total_price = (product.price * quantity) if request.user.country == 'Morocco' else (
                        product.price * quantity) + 100
                    products.append((product, quantity, total_price))
    else:
        return jsonify({'error': 'Product Not Found!'}), 404

    if all((product.stock - quantity) < 0 for (
        product, quantity, total_price) in products
    ):
        return jsonify({"error": "The stock of this product not available for Now!"}), 400

    SEND_EMAIL_For_Each_Store = {}

    for (product, quantity, total_price) in products:

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

        # sending msg tell then that your store product is last then reminder stock.
        if product.stock < product.reminder_stock:
            content = Email.create_content_for_low_stock_dedicated(
                owner, product
            )
            Email.sendEmail(owner.email, content)

        if owner.id not in SEND_EMAIL_For_Each_Store.keys():
            SEND_EMAIL_For_Each_Store[owner.id] = [
                (product, quantity, total_price)
            ]
        else:
            SEND_EMAIL_For_Each_Store[owner.id].append(
                (product, quantity, total_price)
            )

    # sending msg to user store tell them he have an order by sending name and phone and address.
    for id, prds in SEND_EMAIL_For_Each_Store.items():
        own = storage.get(User, id)
        content = Email.create_content_for_new_order(
            own, prds, request.user
        )
        Email.sendEmail(own.email, content)
    return jsonify({"message": "Order created successfully"}), 200
