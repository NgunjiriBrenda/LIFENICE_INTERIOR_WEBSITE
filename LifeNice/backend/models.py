from flask_sqlalchemy import SQLAlchemy
from werkeug.security import generate_passoword_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__="users"

    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(129), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, passowrd):
        return check_password_hash(self:password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
        }

class Product(db.Model):
    __tablename__="products"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(30), default="each")
    spec = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "unit": self.unit,
            "spec": self.spec,
            "description": self.description,

        }

class Cart(db.Model):
    __tablename__="carts"

    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("CartItem", backref="cart", cascade="all, delete-orphan")

    def to_dict(self):
        return{
            "id": self.id,
            "items": [item.to_dict() for item in self.items],
        }

class CartItem(db.Model):
    __tablename__="cart_items"

    id = db.Column(db.Integer, primar_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    product = db.relationship("Product")

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.id,
            "quantity": self.quantity,

        }
    
class Order(db.Model):
    __tablename__="orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(30), default="pending")
    shipping_name = db.Column(db.String(120))
    shipping_address = db.Column(db.String(200))
    shipping_city = db.Column(db.String(100))
    shipping_zip = db.Column(db.String(20))
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "shipping_name": self.shipping_name,
            "shipping_address": self.shipping_address,
            "shipping_city": self.shipping_city,
            "shipping_zip": self.shipping_zip,
            "total":self.total,
            "created_at": self.created_at.isormat(),
            "items": [item.to_dict() for item in self.items],
        }
    
class OrderItem(db.Model):
    __tablename__="order_items"

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, db.ForeignKey("orders.id", nullable=False))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", nullable=False))
    quantity = db.Column(db.Integer,nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)

    product = db.relationship("Product")

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.to_dict(),
            "quantity": self.quantity,
            "price_at_purchase": self.price_at_purchase,

        }
    