from marshmallow import Schema, fields, validate
from schema.product_schema import ProductSchema

# Define the schema using Schema.from_dict
user_schema = Schema.from_dict({
    'username': fields.String(
        required=True,
        validate=validate.Length(min=3, max=50, error="Username must be between 3 and 50 characters.")
    ),
    'email': fields.String(
        required=True,
        validate=[
            validate.Length(min=5, max=100),
            validate.Regexp(
                r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                error="Invalid email format."
            )
        ]
    ),
    'password': fields.String(
        required=False,
        validate=validate.Length(min=6, error="Password must be at least 6 characters long."),
        allow_none=True
    ),
    "isGoogleAuth": fields.Boolean(required=False),
    "email_token": fields.String(
        required=False,
        allow_none=True
    ),
    "subscription_code": fields.String(
        required=False,
        allow_none=True
    ),
    "products": fields.List(fields.Nested(ProductSchema), required=False, description="List of products being tracked")
})
