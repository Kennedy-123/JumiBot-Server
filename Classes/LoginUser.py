from flask import session, make_response
from database.db import user_collection
from werkzeug.security import check_password_hash


class Login:
    @staticmethod
    def login_user(email, password):
        try:
            # Check if email is provided
            if not email:
                return make_response({"success": False, "message": 'Enter email'}, 400)

            # Check if password is provided
            elif not password:
                return make_response({"success": False, "message": "Enter password"}, 400)

            # Query the database for a user with the provided email
            user = user_collection.find_one({"email": email})
            if not user:  # If no user is found, return an error message
                return make_response({'success': False, 'message': "You don't have an account"}, 404)

            # Extract the stored hashed password
            user_password = user['password']

            # Verify the provided password against the stored hashed password
            if not check_password_hash(user_password, password):
                return make_response({'success': False, 'message': 'Incorrect credentials'}, 401)

            session.permanent = True  # allows you to configure a specific expiration time for the session

            # Set session data to track the logged-in user
            session['user_email'] = user['email']  # Store email in session

            # Create a response object to set cookies
            response = make_response({'success': True, 'message': 'Login successfully'}, 200)

            return response
        except:
            return make_response({"success": False, "message": 'An unexpected error occurred. Please try again later.'}, 500)
