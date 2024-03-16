from marshmallow import Schema, fields, EXCLUDE


class UserMetadata(Schema):
    cart_info = fields.List(fields.Dict(), missing=[], required=False)
    address_info = fields.Dict(required=False)


class UserSchema(Schema):
    user_id = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    role = fields.String(required=True)
    user_metadata = fields.Nested(UserMetadata, missing={})
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    status = fields.String(required=True)


class UserUpdateSchema(Schema):
    username = fields.String(required=False)
    email = fields.Email(required=False)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    user_metadata = fields.Nested(UserMetadata, required=False)
    status = fields.String(required=False)


class CategorySchema(Schema):
    category_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    status = fields.String(required=True)
    image_path = fields.String(required=True)
    # metadata = fields.Dict(missing={})
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategoryUpdateSchema(Schema):
    name = fields.String(required=False)
    description = fields.String(required=False)
    status = fields.String(required=False)
    image_path = fields.String(required=False)
    # metadata = fields.Dict(missing={})


class ProductSchema(Schema):
    product_id = fields.String(required=True)
    category_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    stock = fields.Integer(required=True)
    status = fields.String(required=True)
    price = fields.Integer(required=True)
    weight = fields.Float(required=True)
    image_path = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProductUpdateSchema(Schema):
    name = fields.String(required=False)
    description = fields.String(required=False)
    stock = fields.Integer(required=False)
    status = fields.String(required=False)
    price = fields.Integer(required=False)
    weight = fields.Float(required=False)
    image_path = fields.String(required=False)


class AddressSchema(Schema):
    address_id = fields.String(required=True)
    user_id = fields.String(required=True)
    address = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    pincode = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OrderSchema(Schema):
    order_id = fields.String(required=True)
    user_id = fields.String(required=True)
    order_info = fields.Dict(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


user_schema = UserSchema(unknown=EXCLUDE)
category_schema = CategorySchema(unknown=EXCLUDE)
categories_schema = CategorySchema(unknown=EXCLUDE, many=True)
category_update_schema = CategoryUpdateSchema(unknown=EXCLUDE)

product_schema = ProductSchema(unknown=EXCLUDE)
products_schema = ProductSchema(unknown=EXCLUDE, many=True)
product_update_schema = ProductUpdateSchema(unknown=EXCLUDE)

address_schema = AddressSchema(unknown=EXCLUDE)
addresses_schema = AddressSchema(unknown=EXCLUDE, many=True)

user_metadata_schema = UserMetadata(unknown=EXCLUDE)
user_update_schema = UserUpdateSchema(unknown=EXCLUDE)

order_schema = OrderSchema(unknown=EXCLUDE)
orders_schema = OrderSchema(unknown=EXCLUDE, many=True)
