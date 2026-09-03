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


    
