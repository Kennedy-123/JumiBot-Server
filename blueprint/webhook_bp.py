from flask import Blueprint
from flask import request, jsonify, make_response
from database.db import user_collection
import logging

webhook_bp = Blueprint('webhook', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


@webhook_bp.post('/webhook')
def webhook():
    # Paystack sends webhook events here
    data = request.get_json()
    event = data.get("event")

    if event == "subscription.create":
        # Handle new subscription
        subscription_code = data['data']['subscription_code']
        email_token = data['data']['email_token']
        customer_email = data['data']['customer']['email']

        user_collection.update_one(
            {"email": customer_email},  # Match user by email
            {
                "$set": {
                    "subscription_code": subscription_code,
                    "email_token": email_token
                }
            }
        )

    elif event == "subscription.not_renew":
        # Handle subscription cancellation
        customer_email = data['data']['customer']['email']

        # Clear the subscription details in the database
        user_collection.update_one(
            {"email": customer_email},
            {"$set": {
                "subscription_code": None,
                "email_token": None
            }}
        )
    else:
        logging.warning("Unhandled event:", event)

    return jsonify({"status": "success"}), 200
