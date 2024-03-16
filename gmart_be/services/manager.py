from flask import Blueprint, request
from utils.req_schema import product_creation_req_schema, product_update_req_schema
from controllers.admin import ProductController
from utils.authorize import role_required
from utils.constants import Role
from flask_jwt_extended import jwt_required

manager_services = Blueprint("manager_services", __name__)


# Manager Add Product to Category
@manager_services.route('/categories/<category_id>/product', methods=['GET', 'POST'])
@jwt_required()
@role_required([Role.manager.value])
def add_product_to_category(category_id):
    # print(request.get_json())
    payload = request.get_json()
    payload["category_id"] = category_id
    payload = product_creation_req_schema.load(payload)
    res = ProductController.create(payload=payload)
    return res


@manager_services.route('/category/<category_id>/products', methods=['GET'])
@jwt_required()
@role_required([Role.customer.value, Role.manager.value])
def get_products_by_category_id(category_id):
    res = ProductController.get_all_products(category_id=category_id)
    return res


@manager_services.route('/categories/<category_id>/product/<product_id>', methods=['GET', 'PUT'])
@jwt_required()
@role_required([Role.manager.value])
def update_product_in_category(category_id, product_id):
    print(request.get_json())
    payload = product_update_req_schema.load(request.get_json())
    print(payload)
    res = ProductController.update_product(category_id=category_id, product_id=product_id, payload=payload)
    return res


@manager_services.route('/category/<category_id>/product/<product_id>', methods=['DELETE'])
@jwt_required()
@role_required([Role.manager.value])
def remove_product_from_category(category_id, product_id):
    res = ProductController.delete_product(category_id=category_id, product_id=product_id)
    return res
