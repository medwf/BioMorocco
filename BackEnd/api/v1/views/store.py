from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from bcrypt import checkpw


@app_views.route("/store", methods=['GET'], strict_slashes=False)
def yourStore():
    """get store data"""
    store = request.user.store
    if store:
        return jsonify({
            "store": store.to_dict(),
            "categories": [ctg.to_dict() for ctg in store.categories]
        }), 200
    return jsonify({"error": "not store found create one!"}), 400


@app_views.route("/store", methods=['PUT'], strict_slashes=False)
def updateStore():
    """update store data"""
    from api.v1.utils.image import upload_image
    import json

    data = request.form.get("data", None)
    if data:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = None

    if not data and 'file' not in request.files:
        return jsonify({"error": "check your data send!"})

    store = request.user.store
    if store:
        if data:
            storage.update(store, **data)
        upload_image(request, store)
        return jsonify({"message": "Store data updated successfully"}), 200
    return jsonify({"error": "Not store found create one!"}), 400


@app_views.route("/store", methods=['POST'], strict_slashes=False)
def createStore():
    """get store data"""
    from models.store import Store
    from api.v1.utils.image import upload_image
    import json

    data = request.form.get("data", None)
    if data:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = None

    if not data and 'file' not in request.files:
        return jsonify({"error": "check your data send!"})

    store = request.user.store
    if not store:
        if 'name' in data and 'description' in data:
            store = Store(
                user_id=request.user.id,
                name=data['name'],
                description=data['description']
            )

            store.save()
            upload_image(request, store)
            return jsonify({"message": "Store created successfully"}), 200
        return jsonify({"error": "Name and description is mandatory"}), 400
    return jsonify({"error": "You have One!"}), 400


@app_views.route("/store", methods=['DELETE'], strict_slashes=False)
def deleteStore():
    """delete store"""
    from api.v1.utils.image import deleted_image
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "check your data send!"}), 400

    store = request.user.store
    if store:
        if 'password' in data and checkpw(data['password'].encode(), request.user.password.encode()):
            for ctg in store.categories:
                for prd in ctg.products:
                    for rev in prd.reviews:
                        rev.delete()
                    prd.delete()
                ctg.delete()
            deleted_image(store)
            store.delete()
            storage.save()
            return jsonify({"message": "Store deleted successfully"}), 200
        return jsonify({"error": "Your password incorrect"}), 400
    return jsonify({"error": "Not store found create one!"}), 400
