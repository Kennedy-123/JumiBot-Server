from flask import jsonify, Blueprint, request

check_subscription_status_bp = Blueprint('check_subscription_status', __name__)


@check_subscription_status_bp.get('/check_subscription_status')
def check_subscription_status():
    # Get the subscription token from the cookies
    subscription_token = request.cookies.get('basic_subscription_token')

    if subscription_token:
        return jsonify({'subscribed': True}), 200
    else:
        return jsonify({'subscribed': False}), 200
