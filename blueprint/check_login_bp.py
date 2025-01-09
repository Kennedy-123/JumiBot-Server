from flask import jsonify, Blueprint, session

check_login_bp = Blueprint('check-login', __name__, url_prefix='/check-login')


@check_login_bp.route('', methods=['GET'])
def check_login():
    if 'user_email' in session:
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 200
