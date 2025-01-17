from flask import Blueprint
from flask import jsonify, request, make_response
import requests
import os
from dotenv import load_dotenv
import secrets

# Load the .env file
load_dotenv()

callback_bp = Blueprint('callback', __name__, url_prefix='/callback')

PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_BASE_URL = "https://api.paystack.co"


@callback_bp.route('', methods=['GET'])
def handle_callback():
    """
    Paystack appends a reference parameter
    to the callback URL (eg,http://localhost:5000/callback?reference=abc123xyz), which uniquely identifies
    the transaction.
    """
    # Get the transaction reference from query parameters
    reference = request.args.get('reference')

    if not reference:
        return jsonify({"status": False, "message": "No reference provided"}), 400

    # Verify the transaction
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    response = requests.get(f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}", headers=headers)

    if response.status_code == 200:
        transaction_data = response.json()
        if transaction_data['data']['status'] == 'success':
            # Extract email and plan code from metadata
            email = transaction_data['data']['customer']['email']
            plan_code = transaction_data['data']['metadata']['plan_code']

            # Create the subscription using the /subscription endpoint
            subscription_payload = {"customer": email, "plan": plan_code}
            subscription_response = requests.post(
                f"{PAYSTACK_BASE_URL}/subscription",
                json=subscription_payload,
                headers=headers
            )

            # Generate a token
            subscription_token = secrets.token_hex(32)

            if subscription_response.status_code == 200:
                response = make_response(jsonify({
                    "status": True,
                    "reference": reference,
                    "amount": transaction_data['data']['amount'] / 100,
                    "message": "Subscription created successfully",
                    "data": subscription_response.json(),
                }), 200)

                response.set_cookie(
                    "basic_subscription_token",
                    subscription_token,
                    httponly=True,
                    secure=False,  # Use True in production with HTTPS
                    samesite="Lax",
                    max_age=30 * 24 * 60 * 60  # Cookie valid for 30 days
                )

                return response
            else:
                return jsonify({
                    "status": False,
                    "message": "Payment successful but subscription creation failed",
                    "error": subscription_response.json(),
                }), 400
        else:
            return jsonify({"status": False, "message": "Payment failed"}), 400
    else:
        return jsonify({"status": False, "message": "Transaction verification failed"}), 400
