from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import WishList
from models.product import Product


@app_views.route('/wishlists/<int:wishlist_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/wishlists', methods=['GET'], strict_slashes=False)
def wishlist(wishlist_id=None):
    """get wishlists based on session id"""
    from models import storage
    if wishlist_id:
        wishlist = storage.get(WishList, wishlist_id)
        if wishlist and wishlist in request.user.wishlists:
            return jsonify({
                'wishlist': wishlist.to_dict()
            })
        abort(404)
    return jsonify({
        'wishlists': [wsh.to_dict() for wsh in request.user.wishlists]
    }), 200


@app_views.route('/wishlists', methods=['POST'], strict_slashes=False)
def CreateWishlist():
    """create wishlist"""
    from models import storage

    data = request.get_json(silent=True, force=True)
    if data and 'product_id' in data:
        if storage.get(Product, data['product_id']):
            wsh = WishList(
                product_id=data['product_id'],
                user_id=request.user.id
            )
            wsh.save()
            return jsonify({'message': 'products added Successfully'}), 200
        return jsonify({'error': 'products Not Found'}), 404
    return jsonify({'error': 'check your data send'}), 400


@app_views.route('/wishlists/<int:wishlist_id>', methods=['DELETE'], strict_slashes=False)
def deleteWishlist(wishlist_id):
    """delete wishlist"""
    from models import storage

    wsh = storage.get(WishList, wishlist_id)
    if wsh and wsh in request.user.wishlists:
        storage.delete(wsh)
        return jsonify({'message': 'wishlist was deleted successfully'}), 200
    return jsonify({'error': 'wishlist Not Found'}), 404
