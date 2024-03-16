from marshmallow import EXCLUDE, fields, Schema, post_load
from utils.image_utils import get_image_path


class UserCreationReq(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    role = fields.String(required=True)


class CategoryCreationReq(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    image_path = fields.String(required=True)
    status = fields.String(required=True)

    @post_load
    def modify_image_path(self, data, **kwargs):
        data["image_path"] = get_image_path(raw_path=data["image_path"])
        return data


class CategoryUpdateReq(Schema):
    name = fields.String(required=False)
    description = fields.String(required=False)
    image_path = fields.String(required=False)
    status = fields.String(required=False)

    @post_load
    def modify_image_path(self, data, **kwargs):
        if "image_path" in data:
            data["image_path"] = get_image_path(raw_path=data["image_path"])
        return data


class ProductCreationReq(Schema):
    name = fields.String(required=True)
    category_id = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Integer(required=True)
    stock = fields.Integer(required=True)
    weight = fields.Float(required=True)
    image_path = fields.String(required=True)
    status = fields.String(required=True)

    @post_load
    def modify_image_path(self, data, **kwargs):
        if "image_path" in data:
            data["image_path"] = get_image_path(raw_path=data["image_path"])
        return data


class ProductUpdateReq(Schema):
    name = fields.String(required=False)
    description = fields.String(required=False)
    price = fields.String(required=False)
    stock = fields.String(required=False)
    weight = fields.String(required=False)
    image_path = fields.String(required=False)
    status = fields.String(required=False)

    @post_load
    def modify_image_path(self, data, **kwargs):
        if "image_path" in data:
            data["image_path"] = get_image_path(raw_path=data["image_path"])
        return data


class CartUpdateSchema(Schema):
    product_id = fields.String(required=True)
    count = fields.Integer(required=True)


class AddressCreationReq(Schema):
    address = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    pincode = fields.String(required=True)


user_creation_req_schema = UserCreationReq(unknown=EXCLUDE)
category_creation_req_schema = CategoryCreationReq(unknown=EXCLUDE)
category_update_req_schema = CategoryUpdateReq(unknown=EXCLUDE)
product_creation_req_schema = ProductCreationReq(unknown=EXCLUDE)
product_update_req_schema = ProductUpdateReq(unknown=EXCLUDE)
cart_update_schema = CartUpdateSchema(unknown=EXCLUDE)
address_creation_req_schema = AddressCreationReq(unknown=EXCLUDE)
