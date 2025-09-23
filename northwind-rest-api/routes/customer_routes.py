# routes/customer_routes.py
from flask import Blueprint
from controllers import customers

customer_bp = Blueprint("customer_bp", __name__)

customer_bp.route("/", methods=["GET"])(customers.list_customers)
customer_bp.route("/<customer_id>", methods=["GET"])(customers.get_customer)
customer_bp.route("/", methods=["POST"])(customers.create_customer)
customer_bp.route("/<customer_id>", methods=["PUT"])(customers.update_customer)
customer_bp.route("/<customer_id>", methods=["DELETE"])(customers.delete_customer)
