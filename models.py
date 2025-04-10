from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    quantity_in_stock = db.Column(db.Integer, default=0)

class Supplier(db.Model):
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(255))
    address = db.Column(db.String(255))

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    supplier = db.relationship('Supplier', backref=db.backref('orders', lazy=True))

class OrderDetail(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    order = db.relationship('Order', backref=db.backref('order_details', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_details', lazy=True))

class InventoryTransaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # IN or OUT
    quantity_changed = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref=db.backref('transactions', lazy=True))
