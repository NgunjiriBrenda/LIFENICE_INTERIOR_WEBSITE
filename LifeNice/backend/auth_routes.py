import jwt
import datetime
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from models import db, User

auth_bp = Blueprint("auth", __name__)

def make_tokens(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),

    }

    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

def token_required(f):
    """Decorator for routes that need a logged-in user.
    Reads the JWT from Authorization header: 'Bearer <token>'."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header  = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or malformed token"}), 401
        
        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(
                token, current_app.config["JWT_SECRET"], algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired, please log in again"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"error": "User no longer exists"}), 401
        
        return f(user, *args, **kwargs)
    
    return wrapper

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are all required" }), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with that email already exists"}), 409
    

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = make_tokens(user)
    return jsonify({"token": token, "user": user.to_dict()}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Incorrect email or password"}), 401


    token = make_tokens(user)
    return jsonify({"token": token, "user": user.to_dict()}), 200

@auth_bp.route("/me", methods=["GET"])
@token_required
def me(current_user):
    return jsonify({"user": current_user.to_dict()}), 200
