import os
from dotenv import load_dotenv
import requests
from flask import jsonify


# Load the .env file
load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_BASE_URL = "https://api.paystack.co"


class Payment:
    @staticmethod
    def initialize_payment(email, amount, plan_code):
        # Initialize transaction
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": email,
            "amount": amount,  # Amount in kobo
            "currency": "NGN",  # Change this to USD if you're using USD
            "callback_url": "https://jumibot-client.onrender.com//payment-success",  # Your callback URL
            "channels": ["card"],
            "metadata": {"plan_code": plan_code}  # Store the plan code for later reference
        }

        response = requests.post(f"{PAYSTACK_BASE_URL}/transaction/initialize", json=payload, headers=headers)

        try:
            response_data = response.json()
        except ValueError:
            return {"status": False, "message": "Invalid response from Paystack"}, 500

        if response.status_code == 200:
            payment_url = response.json().get('data', {}).get('authorization_url')
            return jsonify({"status": True, "payment_url": payment_url}), 200
        else:
            return jsonify({"status": False, "message": response.json()}), 400
