# routes/order_routes.py
from flask import Blueprint
from controllers import orders

order_bp = Blueprint("orders", __name__)

order_bp.route("/", methods=["GET"])(orders.list_orders)
order_bp.route("/<int:order_id>", methods=["GET"])(orders.get_order)
order_bp.route("/", methods=["POST"])(orders.create_order)
order_bp.route("/<int:order_id>", methods=["PUT"])(orders.update_order)
order_bp.route("/<int:order_id>", methods=["DELETE"])(orders.delete_order)
order_bp.route("/customer/<string:customer_id>", methods=["GET"])(orders.get_customer_orders)
