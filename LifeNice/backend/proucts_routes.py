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


    
