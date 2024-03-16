from .db_engine import DBEngine
from .db_models import User, Category, Product, Address, Order
from .db_schema import user_schema, category_schema, categories_schema, category_update_schema, product_schema, \
    products_schema, product_update_schema, address_schema, addresses_schema, user_metadata_schema, user_update_schema, \
    order_schema, orders_schema


class UserDAO:

    @classmethod
    def create(cls, params):
        print(params)
        user_params = user_schema.load(params)
        with DBEngine.get_db_session() as session:
            session.add(User(**user_params))
        return user_params

    @classmethod
    def get(cls, user_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(User).filter(User.user_id == user_id).one()
            user_info = user_schema.dump(db_obj)
            return user_info

    @classmethod
    def login(cls, username, password, role):
        with DBEngine.get_db_session() as session:
            try:
                customer = session.query(User).filter(User.username == username,
                                                      User.password == password,
                                                      User.role == role).one()
                if customer:
                    return {"username": customer.username, "user_id": customer.user_id, "role": role}
                else:
                    return None
            except:
                pass

    @classmethod
    def update_cart(cls, user_id, product_info):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(User.user_metadata).filter(User.user_id == user_id).one()
            user_metadata = user_metadata_schema.dump(db_obj.user_metadata)
        index_to_update = None
        if user_metadata.get("cart_info"):
            for idx, val in enumerate(user_metadata['cart_info']):
                if val["product_id"] == product_info["product_id"]:
                    index_to_update = idx
                    break
            if index_to_update is not None:
                user_metadata['cart_info'][index_to_update]["count"] += product_info["count"]
            else:
                user_metadata['cart_info'].append(product_info)
        else:
            user_metadata["cart_info"] = []
            user_metadata['cart_info'].append(product_info)
        user_params = {"user_metadata": user_metadata}
        with DBEngine.get_db_session() as session:
            session.query(User).filter(User.user_id == user_id).update(
                user_params)  # cart_info = db_obj.cart_info if db_obj.cart_info else []
        return {"user_id": user_id, "success": True}

    @classmethod
    def remove_cart_item(cls, user_id, product_id_to_remove):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(User.user_metadata).filter(User.user_id == user_id).one()
            user_metadata = user_metadata_schema.dump(db_obj.user_metadata)
        index_to_remove = None
        if user_metadata.get("cart_info"):
            for idx, val in enumerate(user_metadata['cart_info']):
                if val["product_id"] == product_id_to_remove:
                    index_to_remove = idx
                    break
            if index_to_remove is not None:
                user_metadata['cart_info'].pop(index_to_remove)
        else:
            user_metadata["cart_info"] = []
        user_params = {"user_metadata": user_metadata}
        with DBEngine.get_db_session() as session:
            session.query(User).filter(User.user_id == user_id).update(
                user_params)  # cart_info = db_obj.cart_info if db_obj.cart_info else []
        return {"user_id": user_id, "success": True}

    @classmethod
    def update_address_info(cls, user_id, current_address_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(User.user_metadata).filter(User.user_id == user_id).one()
            user_metadata = user_metadata_schema.dump(db_obj.user_metadata)
        user_metadata['address_info'] = {
            'current_address_id': current_address_id
        }
        user_params = {"user_metadata": user_metadata}
        with DBEngine.get_db_session() as session:
            session.query(User).filter(User.user_id == user_id).update(
                user_params)  # cart_info = db_obj.cart_info if db_obj.cart_info else []
        return {"user_id": user_id, "success": True}

    @classmethod
    def update(cls, user_id, params):
        user_update_params = user_update_schema.load(params)
        print(f"User ID: {user_id}, {user_update_params}")
        with (DBEngine.get_db_session() as session):
            session.query(User).filter(User.user_id == user_id).update(user_update_params)
            # update(category_update_params)
        return {"success": True}

    @classmethod
    def remove_from_cart(cls, user_id, product_info):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(User.cart_info).filter(User.user_id == user_id).one()
            cart_info = db_obj.cart_info if db_obj.cart_info else []
        try:
            cart_info.append(product_info)
            cart_info_params = {"cart_info": cart_info}
            with DBEngine.get_db_session() as session:
                session.query(User).filter(User.user_id == user_id).update(
                    cart_info_params)  # cart_info = db_obj.cart_info if db_obj.cart_info else []
        except Exception:
            print("Looks like no such element is present")
        return {"user_id": user_id, "success": True}

    @classmethod
    def get_cart(cls, user_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(User.user_metadata).filter(User.user_id == user_id).one()
            user_metadata = user_metadata_schema.load(db_obj.user_metadata)
            return user_metadata['cart_info']

    @classmethod
    def get_details(cls, product_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(Product).filter(Product.product_id == product_id).one()
            product_details = product_schema.dump(db_obj)
            return product_details

    @classmethod
    def add_address(cls, params):
        address_params = address_schema.load(params)
        with DBEngine.get_db_session() as session:
            session.add(Address(**address_params))
            return address_params

    @classmethod
    def get_addresses(cls, user_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(Address).filter(Address.user_id == user_id).all()
            addresses = addresses_schema.dump(db_obj)
            return addresses

    @classmethod
    def get_address(cls, address_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(Address).filter(Address.address_id == address_id).one()
            address_details = address_schema.dump(db_obj)
            return address_details




class OrderDAO:
    @classmethod
    def create(cls, params):
        print(params)
        order_params = order_schema.load(params)
        with DBEngine.get_db_session() as session:
            session.add(Order(**order_params))
            order_info = order_schema.dump(order_params)
        return order_info

    @classmethod
    def get_orders(cls, user_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
            orders = orders_schema.dump(db_obj)
            return orders

    @classmethod
    def get_order(cls, user_id, order_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(Order).filter(Order.user_id == user_id, Order.order_id==order_id).one()
            order = order_schema.dump(db_obj)
            return order


# on click: done
# 1. update user_metadata (api call) -> data=> current_address_id = selectedAddressId
# 2. push to next page(no need to pass anything)

# on arriving to the next page:
# load user data (api call) => output: user_info
# load address data from address_id (user_info["user_metadata"]["address_info"]["current_address_id"])

# user_info = get_user_info  user_id
# current_address_id = user_info["user_metadata"]["address_info"]["current_address_id"]
# address_info = get_address_info(address_id = current_address_id)
# return {
#     "user_info": user_info,
#     "address_info": address_info
# }

# on clicking to place order: input(user_id)
# 1. Get user_info from user_id
# 2. Create order entry => order_id: uuid, order_info: user_info["user_metadata"](from user_id)
# 3. Update user_metadata to empty dictionary {}
# 4. Return order_info in response

# user_metadata = {
#     "cart_info": [],
#     "address_info": {
#         "current_address_id": ""
#     }
# }


class CategoryDAO:
    @classmethod
    def create(cls, params):
        print(params)
        category_params = category_schema.load(params)
        with DBEngine.get_db_session() as session:
            session.add(Category(**category_params))
        return category_params

    @classmethod
    def get_all_categories(cls, status):
        status_filter = ["ACTIVE", "UPDATION_REQUESTED", "DELETION_REQUESTED"]
        with DBEngine.get_db_session() as session:
            db_rows = session.query(Category).filter(Category.status.in_(status_filter)).all()
            categories = categories_schema.dump(db_rows)
        return categories

    @classmethod
    def get_requested_categories(cls, status):
        with DBEngine.get_db_session() as session:
            db_rows = session.query(Category).filter(Category.status == status).all()
            categories = categories_schema.dump(db_rows)
        return categories

    @classmethod
    def delete_category(cls, category_id, status):
        with DBEngine.get_db_session() as session:
            category = session.query(Category).filter_by(category_id=category_id).first()
            if category:
                category.status = status.value
                return {'success': True, "message": "Category deleted successfully"}
            else:
                return {"success": False, "message": "Category not found"}

    @classmethod
    def update_category(cls, category_id, params):
        category_update_params = category_update_schema.load(params)
        print(f"Category ID: {category_id}, {category_update_params}")
        with (DBEngine.get_db_session() as session):
            session.query(Category).filter(Category.category_id == category_id).update(category_update_params)
            # update(category_update_params)
        return {"success": True}
        # return {}


class ProductDAO:
    @classmethod
    def create(cls, params):
        product_params = product_schema.load(params)
        print(product_params)
        with DBEngine.get_db_session() as session:
            session.add(Product(**product_params))
        return product_params

    @classmethod
    def get(cls, product_id):
        with DBEngine.get_db_session() as session:
            db_obj = session.query(Product).filter(Product.product_id == product_id).one()
            product_info = product_schema.dump(db_obj)
            return product_info
    @classmethod
    def get_all_products(cls, category_id, status):
        with DBEngine.get_db_session() as session:
            db_rows = session.query(Product).filter(Product.category_id == category_id,
                                                    Product.status == "ACTIVE").all()
            products = products_schema.dump(db_rows)
        return products

    @classmethod
    def get_requested_categories(cls, status):
        with DBEngine.get_db_session() as session:
            db_rows = session.query(Category).filter(Category.status == status).all()
            categories = categories_schema.dump(db_rows)
        return categories

    @classmethod
    def delete_category(cls, category_id, status):
        with DBEngine.get_db_session() as session:
            category = session.query(Category).filter_by(category_id=category_id).first()
            if category:
                category.status = status.value
                return {'success': True, "message": "Category deleted successfully"}
            else:
                return {"success": False, "message": "Category not found"}

    @classmethod
    def update_product(cls, category_id, product_id, params):
        product_update_params = product_update_schema.load(params)
        with DBEngine.get_db_session() as session:
            session.query(Product).filter(Product.category_id == category_id, Product.product_id == product_id).update(
                product_update_params)
        return {"success": True}
