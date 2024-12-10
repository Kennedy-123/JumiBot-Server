product_schema = {
    "product_name": {"type": "string", "required": True, "empty": False},
    "product_url": {"type": "string", "required": True, "regex": r"^https?:\/\/.*"},
    "current_price": {"type": "float", "required": True, "min": 0},
    "product_image_src": {"type": "string", "required": True, "regex": r"^https?:\/\/[^\s/$.?#].[^\s]*$", "empty": False},
    "last_checked": {"type": "datetime", "required": False}
}
