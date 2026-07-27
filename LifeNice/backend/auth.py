import jwt
import datetime
import functools import wraps
import flask import Blueprint, request, jsonify, current_app
import models import db, User

auth_bp = Blueprint("auth", __name__)

def make_tokens(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime utcnow() + datetime.timedelta(days=7),

    }

    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

def token_required(f):
    """Decorator for routes that need a logged-in user.
    Reads the JWT from Authorization header: 'Bearer <token>'."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header  = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer"):
            return jsonify({"error": "Missing or malformed token"}), 401
        
        token = auth_header.split("", 1)[1]
        try:
            payload = jwt.decode(
                token, current_app.config["JWT_SECRET"], algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired, please log in again"})
