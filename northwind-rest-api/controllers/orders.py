# controllers/orders.py
from flask import jsonify, request
from config import db
from models.order import Order
from schemas.order_schema import OrderSchema
from pydantic import ValidationError

# Listing all orders
def list_orders():
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    orders = Order.query.limit(limit).offset(offset).all()
    return jsonify([o.to_dict() for o in orders]), 200

# Retrieving single order by ID
def get_order(order_id):
    o = db.session.get(Order, order_id)
    if not o:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(o.to_dict()), 200

# Creating new order with validation
def create_order():
    try:
        payload = request.get_json(force=True)
        schema = OrderSchema(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 400

    if db.session.get(Order, schema.OrderID):
        return jsonify({"error": "Order with this ID already exists"}), 409

    new_order = Order(**schema.model_dump())
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

# Updating order details with validation
def update_order(order_id):
    o = db.session.get(Order, order_id)
    if not o:
        return jsonify({"error": "Order not found"}), 404

    try:
        payload = request.get_json(force=True)
        payload["OrderID"] = order_id
        schema = OrderSchema(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 400

    for k, v in schema.model_dump().items():
        setattr(o, k, v)
    db.session.commit()
    return jsonify(o.to_dict()), 200

# Deleting order by ID
def delete_order(order_id):
    o = db.session.get(Order, order_id)
    if not o:
        return jsonify({"error": "Order not found"}), 404
    db.session.delete(o)
    db.session.commit()
    return jsonify({"message": f"Order {order_id} deleted"}), 200

# Retrieving all orders for a single customer by ID
def get_customer_orders(customer_id):
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    orders = Order.query.filter_by(CustomerID=customer_id).limit(limit).offset(offset).all()
    if not orders:
        return jsonify({"error": f"No orders found for customer {customer_id}"}), 404
    
    return jsonify([o.to_dict() for o in orders]), 200
