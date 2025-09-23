# app.py
from flask import Flask
from config import db, Config


def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config:
        app.config.from_mapping(test_config)
    else:
        # Config from config.py
        app.config.from_object(Config)

    # Init db
    db.init_app(app)

    # Register routes
    with app.app_context():
        from routes.customer_routes import customer_bp
        from routes.product_routes import product_bp
        from routes.order_routes import order_bp
        app.register_blueprint(customer_bp, url_prefix="/customers")
        app.register_blueprint(product_bp, url_prefix="/products")
        app.register_blueprint(order_bp, url_prefix="/orders")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
