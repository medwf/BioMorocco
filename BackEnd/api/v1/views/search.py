from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import Search


@app_views.route('/searches/<int:search_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/searches', methods=['GET'], strict_slashes=False)
def search(search_id=None):
    """get searches based on session id"""
    from models import storage
    if search_id:
        search = storage.get(Search, search_id)
        if search and search in request.user.searches:
            return jsonify({
                'search': search.to_dict()
            })
        abort(404)
    return jsonify({
        'searches': [srx.to_dict() for srx in request.user.searches]
    }), 200


@app_views.route('/searches', methods=['POST'], strict_slashes=False)
def CreateSearch():
    """create Search"""
    import json

    data = request.get_json(silent=True, force=True)

    if data and 'name' in data:
        print(data)
        srx = Search(
            name=data['name'],
            user_id=request.user.id
        )
        srx.save()
        return jsonify({'message': 'Search name added Successfully'}), 200
    return jsonify({'error': 'check your data send'}), 400


@app_views.route('/searches/<int:search_id>', methods=['DELETE'], strict_slashes=False)
def deleteSearch(search_id):
    """delete Search"""
    from models import storage

    search = storage.get(Search, search_id)
    if search and search in request.user.searches:
        storage.delete(search)
        storage.save()
        return jsonify({'message': 'Search name was deleted successfully'}), 200
    return jsonify({'error': 'Search Not Found'}), 404
