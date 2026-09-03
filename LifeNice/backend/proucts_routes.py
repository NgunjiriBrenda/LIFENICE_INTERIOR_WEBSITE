from flask import Blueprint, request, jsonify
from models import db, Product
from auth_routes import token_required, admin_required

products_bp = Blueprint("products", __name__)

@products_bp.route("/products" ,methods=["GET"])
def list_products():
    category = request.args.get("category")
    query = Product.query
    if category: 
        query = query.filter_by(category=category)
    products = query.all()
    return jsonify([p.to_dict() for p in products]), 200

@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

@products_bp.route("/products", methods=["POST"])
@token_required
@admin_required
def create_product(current_user):
    data = request.get_json(silent=True) or {}
    required_fields = ["sku", "name", "category", "price", "stock"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    product = Product(
        sku=data["sku"],
        name=data["name"],
        category=data["category"],
        price=data["price"],
        unit=data.get("unit", "each"),
        spec=data.get("spec"),
        description=data.get("description"),
        stock=data["stock"],
        image_url=data.get("image_url")
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@products_bp.route("/products/<int:product_id>", methods=["PUT"])
@token_required
@admin_required

def update_product(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json(silent=True) or {}
    for field in ["sku", "name", "category", "price", "unit", "spec", "description", "stock", "image_url"]:
        if field in data:
            setattr(product, field, data[field])

    db.session.commit()
    return jsonify(product.to_dict()), 200

@products_bp.route("/products/<int:product_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_product(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

