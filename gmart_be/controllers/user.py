from db.dao import UserDAO, OrderDAO, ProductDAO, CategoryDAO
import uuid
from typing import Dict, Any
from flask_jwt_extended import create_access_token


class UserController:

    @classmethod
    def create(cls, payload):
        payload["user_id"] = str(uuid.uuid4())
        payload["status"] = "ACTIVE"
        res = UserDAO.create(params=payload)
        print("res", res)
        return {"user_id": res["user_id"], "success": True}

    @classmethod
    def get_user_by_id(cls, user_id):
        user_info = UserDAO.get(user_id=user_id)
        return {"user_info": user_info, "success": True}

    @classmethod
    def get_user_by_credential(cls, data):
        username = data['userName']
        password = data['password']
        role = data['role']
        user_details = UserDAO.login(username=username, password=password, role=role)

        if user_details:
            access_token = create_access_token(identity=username, additional_claims={'role': user_details["role"]})
            return {**user_details, 'access_token': access_token, 'message': 'Login successful', 'success': True}
        else:
            return {"success": False, "message": "Incorrect credentials"}

    @classmethod
    def add_to_cart(cls, user_id, product_info):
        res = UserDAO.update_cart(user_id=user_id, product_info=product_info)
        return res

    @classmethod
    def remove_from_cart(cls, user_id, payload):
        res = UserDAO.remove_cart_item(user_id=user_id, product_id_to_remove=payload["product_id"])
        return res

    @classmethod
    def get_cart_info(cls, user_id):
        cart_info = UserDAO.get_cart(user_id=user_id)
        return cart_info

    @classmethod
    def get_product(cls, product_id):
        product = UserDAO.get_details(product_id=product_id)
        return product

    @classmethod
    def add_address(cls, user_id, payload):
        payload['user_id'] = user_id
        payload['address_id'] = str(uuid.uuid4())
        res = UserDAO.add_address(params=payload)
        return res

    @classmethod
    def get_addresses(cls, user_id):
        addresses = UserDAO.get_addresses(user_id=user_id)
        return addresses

    @classmethod
    def update_current_address(cls, user_id, payload):
        current_address_id = payload['current_address_id']
        res = UserDAO.update_address_info(user_id=user_id, current_address_id=current_address_id)
        return res

    @classmethod
    def get_cart_summary(cls, user_id):
        user_info = UserDAO.get(user_id=user_id)
        current_address_id = user_info["user_metadata"]["address_info"]["current_address_id"]
        address_info = UserDAO.get_address(address_id=current_address_id)
        res = {
            "user_info": user_info,
            "address_info": address_info
        }
        return res

    @classmethod
    def place_order(cls, user_id):
        order_creation_params = {}
        order_creation_params["order_id"] = str(uuid.uuid4())
        order_creation_params["user_id"] = user_id
        # 1. Get user_info from user_id
        user_info = UserDAO.get(user_id=user_id)
        user_metadata = user_info["user_metadata"]
        order_creation_params["order_info"] = user_metadata
        order_creation_params["status"] = "PLACED"
        # 2. Create order entry => order_id: uuid, order_info: user_info["user_metadata"](from user_id)
        order_info = OrderDAO.create(params=order_creation_params)
        # 3. Update user_metadata to empty dictionary {}
        user_update_params = {
            "user_metadata": {}
        }
        UserDAO.update(user_id=user_id, params=user_update_params)
        # 4. Update product stock
        for cart_item in user_metadata["cart_info"]:
            product_id = cart_item["product_id"]
            product_info = ProductDAO.get(product_id=product_id)
            updated_stock = product_info["stock"] - cart_item["count"]
            product_update_params = {"stock": updated_stock}
            category_id = product_info["category_id"]
            ProductDAO.update_product(category_id=category_id, product_id=product_id, params=product_update_params)
        return order_info

    @classmethod
    def get_orders(cls, user_id):

        orders = OrderDAO.get_orders(user_id)
        orders_res = []
        for order in orders:
            total_order_amount = 0
            order_info = order["order_info"]
            products_info = []
            for item in order_info["cart_info"]:
                product_item = {}
                product_id = item["product_id"]
                product_info = ProductDAO.get(product_id=product_id)  # implement this function
                product_item["price"] = product_info["price"]
                product_item["count"] = item["count"]
                product_amount = product_info["price"] * item["count"]
                total_order_amount += product_amount
                product_item["product_amount"] = product_amount
                product_item["name"] = product_info["name"]
                products_info.append(product_item)
            address_id = order_info["address_info"]["current_address_id"]
            address_info = UserDAO.get_address(address_id=address_id)
            order_res = {
                "order_id": order["order_id"],
                "products_info": products_info,
                "address_info": address_info,
                "total_order_amount": total_order_amount,
                "created_at": order['created_at']
            }
            orders_res.append(order_res)
        return orders_res

    @classmethod
    def get_order(cls, user_id, order_id):

        order = OrderDAO.get_order(user_id=user_id, order_id=order_id)
        total_order_amount = 0
        order_info = order["order_info"]
        products_info = []
        for item in order_info["cart_info"]:
            product_item = {}
            product_id = item["product_id"]
            product_info = ProductDAO.get(product_id=product_id)  # implement this function
            product_item["price"] = product_info["price"]
            product_item["count"] = item["count"]
            product_amount = product_info["price"] * item["count"]
            total_order_amount += product_amount
            product_item["product_amount"] = product_amount
            product_item["name"] = product_info["name"]
            products_info.append(product_item)
        address_id = order_info["address_info"]["current_address_id"]
        address_info = UserDAO.get_address(address_id=address_id)
        order_res = {
            "order_id": order["order_id"],
            "products_info": products_info,
            "address_info": address_info,
            "total_order_amount": total_order_amount,
            "created_at": order['created_at']
        }
        return order_res
