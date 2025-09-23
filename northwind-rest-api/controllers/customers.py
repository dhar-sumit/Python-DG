# controllers/customers.py
from flask import jsonify, request
from config import db
from models.customer import Customer
from schemas.customer_schema import CustomerSchema
from pydantic import ValidationError

def list_customers():
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    customers = Customer.query.limit(limit).offset(offset).all()
    return jsonify([c.to_dict() for c in customers]), 200

def get_customer(customer_id):
    c = db.session.get(Customer, customer_id)
    if not c:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(c.to_dict()), 200

def create_customer():
    try:
        payload = request.get_json(force=True)
        schema = CustomerSchema(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 400

    if db.session.get(Customer, schema.CustomerID):
        return jsonify({"error": "Customer with this ID already exists"}), 409

    new_customer = Customer(**schema.model_dump())
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.to_dict()), 201

def update_customer(customer_id):
    c = db.session.get(Customer, customer_id)
    if not c:
        return jsonify({"error": "Customer not found"}), 404

    try:
        payload = request.get_json(force=True)
        payload["CustomerID"] = customer_id
        schema = CustomerSchema(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 400

    for k, v in schema.model_dump().items():
        setattr(c, k, v)
    db.session.commit()
    return jsonify(c.to_dict()), 200

def delete_customer(customer_id):
    c = db.session.get(Customer, customer_id)
    if not c:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": f"Customer {customer_id} deleted"}), 200
