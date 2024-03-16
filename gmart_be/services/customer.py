from flask import Blueprint, request
from utils.constants import Role
from utils.authorize import role_required
from utils.req_schema import user_creation_req_schema, cart_update_schema, address_creation_req_schema
from controllers.user import UserController
from flask_jwt_extended import jwt_required

customer_services = Blueprint("customer_services", __name__)


# Customer login check
@customer_services.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_res = UserController.get_user_by_credential(data=data)
    return login_res


@customer_services.route('/user', methods=['POST'])
def create_customers():
    payload = user_creation_req_schema.load(request.get_json())
    res = UserController.create(payload=payload)
    return res


# @jwt_required
# @role_required([Role.admin.value, Role.customer.value, Role.manager.value])
# @customer_services.route('/categories/<int:category_id>/products', methods=['GET'])
# @jwt_required()
# @role_required([Role.customer.value, Role.manager.value])
# def get_products_in_category(category_id):
#     return f"Products of Category {category_id}"


# @customer_services.route('/categories/<category_id>/products/<product_id>', methods=['GET'])
# def get_product_in_category(category_id, product_id):
#     return f"Product details of product of product id {product_id} of Category {category_id}"


# Customer Add Product to Cart
@customer_services.post('/user/<user_id>/cart')
@jwt_required()
@role_required([Role.customer.value])
def add_to_cart(user_id):
    payload = cart_update_schema.load(request.get_json())
    res = UserController.add_to_cart(user_id=user_id, product_info=payload)
    return res


@customer_services.delete('/user/<user_id>/cart')
@jwt_required()
@role_required([Role.customer.value])
def remove_from_cart(user_id):
    payload = request.get_json()
    print(f"payload {payload}")
    res = UserController.remove_from_cart(user_id=user_id, payload=payload)
    return res


# Customer View Cart
@customer_services.route('/cart/<user_id>', methods=['GET'])
@jwt_required()
@role_required([Role.customer.value])
def view_cart(user_id):
    res = UserController.get_cart_info(user_id=user_id)
    return res


@customer_services.route('/product/<product_id>', methods=['GET'])
@jwt_required()
@role_required([Role.customer.value])
def get_product_details(product_id):
    res = UserController.get_product(product_id=product_id)
    print(res)
    return res


# Get address of a customer
@customer_services.route('/users/<user_id>/addresses', methods=['GET'])
@jwt_required()
@role_required([Role.customer.value])
def get_address(user_id):
    print(user_id)
    res = UserController.get_addresses(user_id=user_id)
    # print(res)
    return res


# Add address of a customer
@customer_services.route('/address/<user_id>', methods=['POST'])
@jwt_required()
@role_required([Role.customer.value])
def add_address(user_id):
    payload = address_creation_req_schema.load(request.get_json())
    res = UserController.add_address(user_id=user_id, payload=payload)
    return res


# update address of a customer
@customer_services.route('/users/<user_id>/address', methods=['PUT'])
@jwt_required()
@role_required([Role.customer.value])
def update_address(user_id):
    payload = request.get_json()
    res = UserController.update_current_address(user_id=user_id, payload=payload)
    return res


@customer_services.route('/user/<user_id>/cart_summary', methods=['GET'])
@jwt_required()
@role_required([Role.customer.value])
def get_cart_summary(user_id):
    res = UserController.get_cart_summary(user_id=user_id)
    # print(res)
    return res


@customer_services.route('/user/<user_id>/place_order', methods=['POST'])
@jwt_required()
@role_required([Role.customer.value])
def create_order(user_id):
    # payload = get_cart_summary(user_id)
    # metadata = payload['user_info']['user_metadata']
    # print(payload['user_info']['user_metadata'])
    res = UserController.place_order(user_id=user_id)
    return res


@customer_services.route('/user/<user_id>/orders', methods=['GET'])
@jwt_required()
@role_required([Role.customer.value])
def get_orders(user_id):
    orders = UserController.get_orders(user_id=user_id)
    return orders


@customer_services.route('/user/<user_id>/orders/<order_id>', methods=['GET'])
@jwt_required()
@role_required([Role.customer.value])
def get_order(user_id, order_id):
    order = UserController.get_order(user_id=user_id, order_id=order_id)
    return order

# # delete address of a customer
# @customer_services.route('/address/<user_id>', methods=['DELETE'])
# def delete_address(user_id):
#     return "Delete a Customer's address"


# # Customer Place Order
# @customer_services.route('/user/<user_id>', methods=['POST'])
# def place_order():
#     return "Place Order"
