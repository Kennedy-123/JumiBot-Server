from marshmallow import Schema, fields, validate

# Product schema definition
ProductSchema = Schema.from_dict({
    "product_name": fields.String(required=True, description="Name of the product"),
    "product_url": fields.String(
        required=True,
        description="URL of the product to track",
        validate=[validate.Regexp(r"^https?:\/\/[^\s/$.?#].[^\s]*$", error="invalid url format")]),
    "current_price": fields.Float(required=True, description="Current price of the product"),
    "product_image_src": fields.String(required=True, validate=[validate.Regexp(r"^https?:\/\/[^\s/$.?#].[^\s]*$")]),
    "last_checked": fields.DateTime(required=False, description="Last time the price was checked"),
})

