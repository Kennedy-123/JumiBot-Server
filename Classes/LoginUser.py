from flask import session, make_response
from database.db import user_collection
from werkzeug.security import check_password_hash


class Login:
    @staticmethod
    def login_user(email, password):
        try:
            # Check if email is provided
            if not email:
                return make_response({"success": False, "error": 'Enter email'})

            # Check if password is provided
            elif not password:
                return make_response({"success": False, "error": "Enter password"})

            # Query the database for a user with the provided email
            user = user_collection.find_one({"email": email})
            if not user:  # If no user is found, return an error message
                return make_response({'success': False, 'error': "You don't have an account"})

            # Extract the stored hashed password
            user_password = user['password']

            # Verify the provided password against the stored hashed password
            if not check_password_hash(user_password, password):
                return make_response({'success': False, 'error': 'Incorrect credentials'})

            # Set session data to track the logged-in user
            session['user_id'] = str(user['_id'])  # Store user ID in session
            session['user_email'] = user['email']  # Store email in session

            session.permanent = True  # allows you to configure a specific expiration time for the session

            # Create a response object to set cookies
            response = make_response({'success': True, 'message': 'Login successfully'})

            # Set cookies for session ID and user email
            response.set_cookie('user_email', user['username'], max_age=3600)  # 1-hour expiry

            return response
        except Exception as e:
            return {"success": False, "message": str(e)}

