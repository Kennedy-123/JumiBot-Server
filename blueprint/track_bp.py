from flask import jsonify, Blueprint, request, session
from Classes.Tracking import Tracking
from datetime import datetime
from schema.product_schema import ProductSchema
from marshmallow import ValidationError
from database.db import user_collection
import threading
from decorators.auth_decorators import login_required

track_bp = Blueprint('track', __name__, url_prefix='/track')


@track_bp.route('/', methods=['POST'])
@login_required
def track_product():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Create an instance of Tracking
        tracker = Tracking(url=url)
        tracker.load_webpage()
        product_details = tracker.get_product_details()

        product_data = {
            "product_name": product_details["product_name"],
            "product_url": product_details["product_url"],
            "current_price": product_details["current_price"],
            "product_image_src": product_details["product_image_src"],
            "last_checked": datetime.now().isoformat()
        }

        # Validate the product data using the schema
        try:
            user_schema_instance = ProductSchema()
            user_schema_instance.load(product_data)  # Validates product data
        except ValidationError as e:
            return jsonify({"success": False, "errors": e.messages}), 400

        # Check if the product already exists in the user's 'products' list
        existing_user = user_collection.find_one(
            {"email": session['user_email']}
        )

        if existing_user:
            products = existing_user.get('products', [])
            product_found = False

            for product in products:
                if product["product_url"] == url:
                    # Update if the price has changed
                    if product["current_price"] > product_details["current_price"]:
                        product["current_price"] = product_data["current_price"]
                    product_found = True

            if not product_found:
                # Add the new product if not found
                products.append(product_data)

            # Update the user document in the database
            user_collection.update_one(
                {"email": session['user_email']},
                {"$set": {"products": products}}
            )
        else:
            # Create a new user document if not found
            new_user = {
                "email": session['user_email'],
                "products": [product_data]
            }
            user_collection.insert_one(new_user)

        # Start the tracking process in a new thread
        user_email = session['user_email']
        tracking_thread = threading.Thread(target=tracker.start_tracking, daemon=True, args=(user_email,))
        tracking_thread.start()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Respond to the user immediately after starting tracking
    return jsonify({"message": "Tracking started successfully"}), 200

