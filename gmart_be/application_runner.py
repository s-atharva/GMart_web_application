from web_app import create_app
from flask_jwt_extended import JWTManager


if __name__ == "__main__":
    app = create_app()
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    jwt = JWTManager(app)
    app.run(port=8005, debug=False)
