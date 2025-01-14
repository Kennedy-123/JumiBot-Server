from flask import jsonify, Blueprint, session
from database.db import user_collection
from decorators.auth_decorators import login_required

tracked_product_bp = Blueprint('tracked_product', __name__, url_prefix='/tracked-product')


@tracked_product_bp.route('', methods=['GET'])
@login_required
def get_tracked_products():
    try:
        # Retrieve user email from the session
        user_email = session.get('user_email')

        # Query the user collection by email
        existing_user = user_collection.find_one({"email": user_email})

        # Serialize the document inline
        existing_user["_id"] = str(existing_user["_id"])  # Convert ObjectId to string

        # Return the serialized document as a JSON response
        return jsonify({"products": existing_user["products"]}), 200

    except:
        return jsonify({'error': 'Please try again later.'}), 500
