# routes/product_routes.py
from flask import Blueprint
from controllers import products

product_bp = Blueprint("product_bp", __name__)

product_bp.route("/", methods=["GET"])(products.list_products)
product_bp.route("/<int:product_id>", methods=["GET"])(products.get_product)
product_bp.route("/", methods=["POST"])(products.create_product)
product_bp.route("/<int:product_id>", methods=["PUT"])(products.update_product)
product_bp.route("/<int:product_id>", methods=["DELETE"])(products.delete_product)
