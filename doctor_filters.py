#!/usr/bin/python3
"""
    Script that starts a Flask web application
"""
from flask import Flask, render_template, jsonify, make_response, request, abort
from models import storage
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(error):
    """
    Handle teardown
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    404 Error handler
    """
    return make_response(jsonify({'error': "Not found"}), 404)

@app.route('/homecare_filters', strict_slashes=False)
def filters_list():
    """
    Method to display homecare filters
    """
    # Assuming you have models for Homecare and Specialization
    states = storage.all('State').values()
    amenities = storage.all('Amenity').values()
    return render_template(
        "10-homecare_filters.html",
        states=states, amenities=amenities)

@app.route('/filter_homecare', methods=['GET'], strict_slashes=False)
def filter_homecare():
    """
    Retrieves the list of all homecare objects based on the provided service type
    """
    service_type = request.args.get("service_type")
    if not service_type:
        abort(400, description="Service type parameter is required")

    homecare_list = storage.get_homecare(service_type)
    homecare_dict = [homecare.to_dict() for homecare in homecare_list]

    return jsonify(homecare_dict)

@app.route('/homecare', methods=['GET'], strict_slashes=False)
def get_homecare():
    """
    Retrieves the list of all homecare objects
    """
    all_homecare = storage.all('Homecare').values()
    list_homecare = [homecare.to_dict() for homecare in all_homecare]
    return jsonify(list_homecare)

@app.route('/homecare/<homecare_id>', methods=['GET'], strict_slashes=False)
def get_single_homecare(homecare_id):
    """
    Retrieves a homecare object by ID
    """
    homecare = storage.get('Homecare', homecare_id)
    if not homecare:
        abort(404)
    return jsonify(homecare.to_dict())

@app.route('/homecare/<homecare_id>', methods=['DELETE'], strict_slashes=False)
def delete_homecare(homecare_id):
    """
    Deletes a homecare object by ID
    """
    homecare = storage.get('Homecare', homecare_id)
    if not homecare:
        abort(404)

    storage.delete(homecare)
    storage.save()
    return make_response(jsonify({}), 200)

@app.route('/homecare/<homecare_id>', methods=['PUT'], strict_slashes=False)
def update_homecare(homecare_id):
    """
    Updates a homecare object by ID
    """
    homecare = storage.get('Homecare', homecare_id)
    if not homecare:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(homecare, key, value)
    storage.save()
    return make_response(jsonify(homecare.to_dict()), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
