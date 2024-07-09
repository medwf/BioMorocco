from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.product import Product


@app_views.route("/products/<int:product_id>/reviews", methods=['GET'], strict_slashes=False)
@app_views.route("/products/<int:product_id>/reviews/<int:review_id>", methods=['GET'], strict_slashes=False)
def yourReviews(product_id=None, review_id=None):
    """get category data"""
    if product_id and review_id:
        rvw = storage.get(Review, review_id)
        if rvw:
            return jsonify({'review': rvw.to_dict()})
    else:
        product = storage.get(Product, product_id)
        if product:
            return jsonify({"reviews": [rvw.to_dict() for rvw in product.reviews]}), 200
    abort(404)


@app_views.route("/products/<int:product_id>/reviews", methods=['POST'], strict_slashes=False)
def createReviews(product_id):
    """POST category data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    product = storage.get(Product, product_id)
    if product:
        if 'rating' in data:
            rev = Review(
                rating=data['rating'],
                product_id=product_id,
                user_id=request.user.id
            )
            storage.update(rev, **data)
            return jsonify({"message": "Review created successfully"}), 200
        return jsonify({"error": "rating is mandatory"}), 400
    return jsonify({"error": "product Not Found!"}), 404


@app_views.route("/reviews/<int:review_id>", methods=['PUT'], strict_slashes=False)
def updateReviews(review_id: int):
    """update category data"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    review = storage.get(Review, review_id)
    if review:
        storage.update(review, **data)
        return jsonify({"message": "review updated successfully"}), 200
    abort(404)


@app_views.route("/reviews/<int:review_id>", methods=['DELETE'], strict_slashes=False)
def deleteReviews(review_id: int):
    """delete category"""

    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({"message": "review deleted successfully"}), 200
    abort(404)
