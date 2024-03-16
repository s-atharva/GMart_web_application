from flask import Blueprint, request
from utils.req_schema import category_creation_req_schema, category_update_req_schema
from controllers.admin import CategoryController
from flask_jwt_extended import jwt_required
from utils.authorize import role_required
from utils.constants import Role

category_services = Blueprint("category_services", __name__)


# Admin Home Page - List of Categories
@category_services.route('/categories', methods=['GET'])
@jwt_required()
@role_required([Role.admin.value, Role.customer.value, Role.manager.value])
def get_categories():
    res = CategoryController.get_all_categories()
    print(res)
    return res


@category_services.route('/categories/requested', methods=['GET'])
@jwt_required()
@role_required([Role.admin.value])
def get_requested_categories():
    res = CategoryController.get_requested_categories()
    return res


# Admin Add Category Page
@category_services.route('/categories/add', methods=['GET', 'POST'])
@jwt_required()
@role_required([Role.admin.value, Role.manager.value])
def add_category():
    print(request.get_json())
    payload = category_creation_req_schema.load(request.get_json())
    print(payload)
    res = CategoryController.create(payload=payload)
    return res


# Admin Update Category Page
@category_services.route('/categories/<category_id>', methods=['PUT'])
@jwt_required()
@role_required([Role.admin.value])
def update_category(category_id):
    payload = category_update_req_schema.load(request.get_json())
    print("update", payload)
    res = CategoryController.update_category(category_id=category_id, payload=payload)
    return res


# Admin Delete Category
@category_services.route('/categories/delete/<category_id>', methods=['DELETE'])
@jwt_required()
@role_required([Role.admin.value])
def delete_category(category_id):
    res = CategoryController.delete_category(category_id=category_id)
    print(res)
    return res
