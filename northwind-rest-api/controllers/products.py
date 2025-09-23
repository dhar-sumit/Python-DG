# controllers/products.py
from flask import jsonify, request
from config import db
from models.product import Product
from schemas.product_schema import ProductSchema
from pydantic import ValidationError

# Listing all products
def list_products():
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    products = Product.query.limit(limit).offset(offset).all()
    return jsonify([p.to_dict() for p in products]), 200

# Retrieving single product by ID
def get_product(product_id):
    p = db.session.get(Product, product_id)
    if not p:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(p.to_dict()), 200

# Creating new product with validation
def create_product():
    try:
        payload = request.get_json(force=True)
        schema = ProductSchema(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 400

    if db.session.get(Product, schema.ProductID):
        return jsonify({"error": "Product with this ID already exists"}), 409

    new_product = Product(**schema.model_dump())
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# Updating product details with validation
def update_product(product_id):
    p = db.session.get(Product, product_id)
    if not p:
        return jsonify({"error": "Product not found"}), 404

    try:
        payload = request.get_json(force=True)
        payload["ProductID"] = product_id
        schema = ProductSchema(**payload)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "details": e.errors()}), 400

    for k, v in schema.model_dump().items():
        setattr(p, k, v)
    db.session.commit()
    return jsonify(p.to_dict()), 200

# Deleting product by ID
def delete_product(product_id):
    p = db.session.get(Product, product_id)
    if not p:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": f"Product {product_id} deleted"}), 200
