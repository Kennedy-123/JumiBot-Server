from flask import jsonify, Blueprint, request
from Classes.RegisterUser import UserRegistration

register_bp = Blueprint('register', __name__, url_prefix='/register-user')


@register_bp.route('/', methods=['POST'])
def register_user():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repeat_password = data.get('repeat_password')

        # Check if repeat_password is provided
        if not repeat_password:
            return jsonify({'msg': 'enter repeat password'}), 400

        # Check if passwords match
        if password != repeat_password:
            return jsonify({'msg': 'Password and repeat password must match'}), 400

        # Validate user input and hash the password if valid
        user_registration = UserRegistration.register_user(username, email, password)

        # If there were validation errors, return them
        if not user_registration["success"]:
            return jsonify({"errors": user_registration["errors"]}), 400

        # when user registration was successful
        return jsonify({'message': user_registration["message"]}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
