from flask import jsonify, Blueprint, request
from Classes.LoginUser import Login

login_bp = Blueprint('login', __name__, url_prefix='/login-user')


@login_bp.route('/', methods=['POST'])
def login_user():
    try:
        # Extract the JSON data sent in the request body
        data = request.json

        # Get the email and password from the JSON data
        email = data.get('email')
        password = data.get('password')

        # login user and get the returned response
        response = Login.login_user(email, password)

        # Return the response returned by the login_user method
        return response
    except Exception as e:
        return jsonify({'msg': str(e)}), 500


