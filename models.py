from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    quantity_in_stock = db.Column(db.Integer, default=0)

class Supplier(db.Model):
    __tablename__ = 'Suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(255))
    address = db.Column(db.String(255))

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('Suppliers.supplier_id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    supplier = db.relationship('Supplier', backref=db.backref('orders', lazy=True))

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'
    detail_id = db.Column(db.Integer, primary_key=True)  # Updated to match DB
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    order = db.relationship('Order', backref=db.backref('order_details', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_details', lazy=True))

class InventoryTransaction(db.Model):
    __tablename__ = 'InventoryTransactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    quantity_changed = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)  # <- match your DB
    notes = db.Column(db.Text)
    product = db.relationship('Product', backref=db.backref('transactions', lazy=True))

