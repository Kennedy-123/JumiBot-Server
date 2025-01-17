from flask import Blueprint
from dotenv import load_dotenv
from flask import request, jsonify, session
from decorators.auth_decorators import login_required
from Classes.Payment import Payment

# Load the .env file
load_dotenv()

subscriptions_bp = Blueprint('subscriptions', __name__)


@subscriptions_bp.route('/subscription', methods=['POST'])
@login_required
def initialize_payment():
    """
    Endpoint to initialize a subscription payment
    """
    # Get user email and subscription plan details from the request
    data = request.get_json()
    email = session.get('user_email')
    amount = data.get("amount")  # Amount in kobo (e.g., 5000 = ₦50)
    plan_code = data.get("plan_code")

    if not email or not amount or not plan_code:
        return jsonify({"status": False, "message": "Email, amount, and plan code are required"}), 400

    return Payment.initialize_payment(email, amount, plan_code)

