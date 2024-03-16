from flask import Flask
from flask_cors import CORS
from services import customer_services, manager_services, category_services
from db.db_models import create_db_models


def register_blueprints(app: Flask):
    app.register_blueprint(customer_services)
    app.register_blueprint(manager_services)
    app.register_blueprint(category_services)


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    CORS(app, resources={r"/*": {'original': "*"}})
    register_blueprints(app=app)
    create_db_models()
    return app
