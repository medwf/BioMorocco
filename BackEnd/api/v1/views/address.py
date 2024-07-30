from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import Address


@app_views.route('/addresses', methods=['GET'], strict_slashes=False)
@app_views.route('/addresses/<int:address_id>', methods=['GET'], strict_slashes=False)
def address(address_id=None):
    """get addresses based on session id"""
    from models import storage
    if address_id:
        address = storage.get(Address, address_id)
        if address and address in request.user.addresses:
            return jsonify({"address": address.to_dict()})
    else:
        return jsonify({
            'addresses': [add.to_dict() for add in request.user.addresses]
        }), 200
    abort(404)


@ app_views.route('/addresses', methods=['POST'], strict_slashes=False)
def CreateAddress():
    """delete session"""
    import json
    data = request.get_json(silent=True, force=True)

    if data:
        if all(dt in data for dt in ('country', 'state', 'city', 'address', 'valid')):
            if 'valid' in data and data['valid']:
                for add in request.user.addresses:
                    add.valid = 0
            address = Address(
                country=data['country'],
                state=data['state'],
                city=data['city'],
                address=data['address'],
                user_id=request.user.id,
                valid=1 if data['valid'] else 0
            )
            address.save()
            return jsonify({'message': 'address created successfully!'}), 200
        return jsonify({'error': 'Enter all data Required'}), 200
    return jsonify({'error': 'check your data send'}), 400


@ app_views.route('/addresses/<int:address_id>', methods=['PUT'], strict_slashes=False)
def UpdateAddress(address_id: int = 0):
    """Update Address"""
    from models import storage
    data = request.get_json(silent=True, force=True)

    if data:
        address = storage.get(Address, address_id)
        if address and address in request.user.addresses:
            if 'valid' in data and data['valid']:
                for add in request.user.addresses:
                    if address_id == add.id:
                        add.valid = 1
                        continue
                    add.valid = 0
                del data['valid']
            storage.update(address, **data)
            return jsonify({'message': 'Your Information updated!'}), 200
        return jsonify({'error': 'Address Not Found'}), 404
    return jsonify({'error': 'check your data send'}), 400


@ app_views.route('/addresses/<int:address_id>', methods=['DELETE'], strict_slashes=False)
def deleteAddress(address_id):
    """delete address"""
    from models import storage

    address = storage.get(Address, address_id)
    if address and address in request.user.addresses:
        if not address.valid:
            storage.delete(address)
            storage.save()
            return jsonify({'message': 'address was deleted successfully'}), 200
        return jsonify({'error': 'change actual address Before delete'}), 400
    return jsonify({'error': 'Address Not Found'}), 404
