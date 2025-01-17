from flask import Blueprint, request, jsonify, session, make_response
from decorators.auth_decorators import login_required
from database.db import user_collection
import requests
import os

cancel_subscription_bp = Blueprint('cancel_subscription', __name__)
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')


@cancel_subscription_bp.get('/cancel-subscription')
@login_required
def cancel_subscription():
    try:
        user_email = session['user_email']
        # Find the user in the database
        user = user_collection.find_one({"email": user_email})

        if not user or not user.get("subscription_code") or not user.get("email_token"):
            return jsonify({"status": "error", "message": "Subscription not found for this user"}), 404

        subscription_code = user["subscription_code"]
        email_token = user["email_token"]

        # Make the request to Paystack to disable the subscription
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "code": subscription_code,
            "token": email_token
        }

        response = requests.post(
            "https://api.paystack.co/subscription/disable",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            res = make_response(jsonify({"status": "success", "message": "Subscription canceled successfully"}), 200)
            res.delete_cookie("basic_subscription_token")
            return res
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to cancel subscription",
                "details": response.json()
            }), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": "An error occurred", "details": str(e)}), 500


