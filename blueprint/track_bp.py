from flask import jsonify, Blueprint, request
from Classes.Tracking import Tracking
from cerberus import Validator
from datetime import datetime
from schema.product_schema import product_schema
from database.db import product_collection
import threading

track_bp = Blueprint('track', __name__, url_prefix='/track')


@track_bp.route('/', methods=['POST'])
def track_product():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Create an instance of Tracking
        tracker = Tracking(url=url)
        tracker.load_webpage()
        product_details = tracker.get_product_details()

        # Validate the product details
        v = Validator(product_schema)
        product_data = {
            "product_name": product_details["product_name"],
            "product_url": product_details["product_url"],
            "current_price": product_details["current_price"],
            "product_image_src": product_details["product_image_src"],
            "last_checked": datetime.now()
        }

        if v.validate(product_data):
            # Check if the product already exists
            existing_product = product_collection.find_one({"product_url": product_details["product_url"]})
            if existing_product:
                # Update if the price has changed
                if existing_product["current_price"] > product_details["current_price"]:
                    product_collection.update_one(
                        {"product_url": product_details["product_url"]},
                        {"$set": {"current_price": product_details["current_price"]}}
                    )
            else:
                product_collection.insert_one(product_data)

        # Start the tracking process in a new thread
        tracking_thread = threading.Thread(target=tracker.start_tracking, daemon=True)
        tracking_thread.start()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Respond to the user immediately after starting tracking
    return jsonify({"message": "Tracking started successfully"}), 200
