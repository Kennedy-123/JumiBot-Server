from schema.user_schema import user_schema
from database.db import user_collection
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from Classes.Email import SendEmail
from flask import session


class UserRegistration:
    @staticmethod
    def register_user(username, email, password, is_google_auth):
        try:
            # Check if username and email already exist
            existing_username = user_collection.find_one({"username": username})
            existing_email = user_collection.find_one({"email": email})
            if not is_google_auth and existing_email:
                return {"success": False, "errors": "Email already exists."}
            elif not is_google_auth and existing_username:
                return {"success": False, "errors": "Username already exists."}

            if not is_google_auth:
                hashed_password = generate_password_hash(password)
                new_user = {
                    'username': username,
                    'email': email,
                    'password': hashed_password,
                    "isGoogleAuth": is_google_auth,
                    "products": []
                }
            else:
                # hashed_password = None  # No password for Google-authenticated users
                new_user = {
                    'username': username,
                    'email': email,
                    "isGoogleAuth": is_google_auth,
                    "products": []
                }

            # Validate the user data using the schema
            try:
                user_schema_instance = user_schema()  # Create schema instance
                user_schema_instance.load(new_user)  # Validate the new user
            except ValidationError as e:
                # Return the custom validation error messages
                return {"success": False, "errors": e.messages}, 400

            if is_google_auth:
                session.permanent = True  # allows you to configure a specific expiration time for the session
                session['user_email'] = email

            # send welcome email
            if not existing_email:
                # Insert the user into the database
                user_collection.insert_one(new_user)

                email_sender = SendEmail()
                email_sender.send_welcome_email(email, username)

            return {"success": True, "message": "User registered successfully."}

        except Exception as e:
            return {"success": False, "message": str(e)}
