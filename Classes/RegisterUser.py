from schema.user_schema import user_schema
from database.db import user_collection
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from Classes.Email import SendEmail


class UserRegistration:
    @staticmethod
    def register_user(username, email, password):
        try:
            # Check if username and email already exist
            existing_username = user_collection.find_one({"username": username})
            existing_email = user_collection.find_one({"email": email})
            if existing_email:
                return {"success": False, "errors": "Email already exists."}
            elif existing_username:
                return {"success": False, "errors": "Username already exists."}

            # Hash the password
            hashed_password = generate_password_hash(password)

            new_user = {
                'username': username,
                'email': email,
                'password': hashed_password,
                "products": []
            }

            # Validate the user data using the schema
            try:
                user_schema_instance = user_schema()  # Create schema instance
                user_schema_instance.load(new_user)  # Validate the new user
            except ValidationError as e:
                # Return the custom validation error messages
                return {"success": False, "errors": e.messages}

            # Insert the user into the database
            user_collection.insert_one(new_user)

            # send welcome email
            email_sender = SendEmail()
            email_sender.send_welcome_email(email, username)

            return {"success": True, "message": "User registered successfully."}

        except Exception as e:
            return {"success": False, "message": str(e)}
