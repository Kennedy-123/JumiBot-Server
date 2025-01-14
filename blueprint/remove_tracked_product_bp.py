from flask import Blueprint, session, request, jsonify
from database.db import user_collection
from decorators.auth_decorators import login_required

remove_product_bp = Blueprint('remove_product', __name__)


@remove_product_bp.route('/remove_product', methods=['DELETE'])
@login_required
def remove_product():
    email = session['user_email']

    try:
        # Extract product_name from the request body
        data = request.get_json()
        product_name = data.get("product_name")

        if not product_name:
            return jsonify({"error": "Product name is required"}), 400

        # Perform the deletion operation
        result = user_collection.update_one(
            {"email": email},  # Match the user by email in the session
            {"$pull": {"products": {"product_name": product_name}}}  # Remove the product
        )

        if result.modified_count > 0:
            return jsonify({"message": "removed successfully"}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except:
        return jsonify({"error": "Please try again later"}), 500
