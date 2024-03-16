from db.dao import CategoryDAO, ProductDAO

from utils.constants import CategoryStatus, ProductStatus
from utils.image_utils import get_image_path

import uuid


class CategoryController:
    @classmethod
    def create(cls, payload):
        payload['category_id'] = str(uuid.uuid4())
        res = CategoryDAO.create(params=payload)
        return {"category_id": res['category_id'], "success": True}

    @classmethod
    def get_all_categories(cls):
        categories = CategoryDAO.get_all_categories(status=CategoryStatus.ACTIVE.value)
        return categories

    @classmethod
    def get_requested_categories(cls):
        categories = CategoryDAO.get_requested_categories(CategoryStatus.REQUESTED.value)
        print(categories)
        return categories

    @classmethod
    def delete_category(cls, category_id):
        result = CategoryDAO.delete_category(category_id, CategoryStatus.DELETED)
        return result

    @classmethod
    def update_category(cls, category_id, payload):
        res = CategoryDAO.update_category(category_id=category_id, params=payload)
        return res


class ProductController:
    @classmethod
    def create(cls, payload):
        payload['product_id'] = str(uuid.uuid4())
        res = ProductDAO.create(params=payload)
        return {"product_id": res['product_id'], "success": True}

    @classmethod
    def get_all_products(cls, category_id):
        products = ProductDAO.get_all_products(category_id, status=ProductStatus.ACTIVE.value)
        return products

    # @classmethod
    # def get_requested_categories(cls):
    #     categories = CategoryDAO.get_requested_categories(CategoryStatus.REQUESTED.value)
    #     print(categories)
    #     return categories
    #
    # @classmethod
    # def delete_category(cls, category_id):
    #     result = CategoryDAO.delete_category(category_id, CategoryStatus.DELETED)
    #     return result

    @classmethod
    def update_product(cls, category_id, product_id, payload):
        payload['product_id'] = product_id
        payload['category_id'] = category_id
        res = ProductDAO.update_product(category_id=category_id, product_id=product_id, params=payload)
        return res

    @classmethod
    def delete_product(cls, category_id, product_id):
        params = {"status": "DELETED", 'product_id': product_id, 'category_id': category_id}
        res = ProductDAO.update_product(category_id=category_id, product_id=product_id, params=params)
        return {'success': True, "message": "Category deleted successfully"}