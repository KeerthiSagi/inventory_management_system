from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Product, Supplier, Order, OrderDetail, InventoryTransaction
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

# ---------- Products ----------
@app.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            quantity_in_stock=int(request.form['quantity_in_stock'])
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.quantity_in_stock = int(request.form['quantity_in_stock'])
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('view_products'))
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('view_products'))

# ---------- Suppliers ----------
@app.route('/suppliers')
def view_suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        supplier = Supplier(
            name=request.form['name'],
            contact_info=request.form['contact_info'],
            address=request.form['address']
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully!')
        return redirect(url_for('view_suppliers'))
    return render_template('add_supplier.html')

@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if request.method == 'POST':
        supplier.name = request.form['name']
        supplier.contact_info = request.form['contact_info']
        supplier.address = request.form['address']
        db.session.commit()
        flash('Supplier updated successfully!')
        return redirect(url_for('view_suppliers'))
    return render_template('edit_supplier.html', supplier=supplier)

@app.route('/delete_supplier/<int:supplier_id>')
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Supplier deleted successfully!')
    return redirect(url_for('view_suppliers'))

# ---------- Orders ----------
@app.route('/orders')
def view_orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    suppliers = Supplier.query.all()
    products = Product.query.all()
    if request.method == 'POST':
        supplier_id = request.form['supplier_id']
        order = Order(supplier_id=supplier_id)
        db.session.add(order)
        db.session.flush()  # to get order_id before commit

        for product in products:
            qty = int(request.form.get(f'quantity_{product.product_id}', 0))
            price = float(request.form.get(f'price_{product.product_id}', 0.0))
            if qty > 0:
                detail = OrderDetail(order_id=order.order_id, product_id=product.product_id, quantity=qty, unit_price=price)
                db.session.add(detail)
                product.quantity_in_stock += qty
        db.session.commit()
        flash('Order placed successfully!')
        return redirect(url_for('view_orders'))

    return render_template('add_order.html', suppliers=suppliers, products=products)

# ---------- Transactions ----------
@app.route('/transactions')
def view_transactions():
    transactions = InventoryTransaction.query.all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    products = Product.query.all()
    if request.method == 'POST':
        product_id = request.form['product_id']
        txn_type = request.form['transaction_type']
        quantity = int(request.form['quantity_changed'])
        notes = request.form['notes']

        # Adjust quantity based on type
        if txn_type == 'OUT':
            quantity = -abs(quantity)
        else:
            quantity = abs(quantity)

        # FIX: Include transaction_date to match your table definition
        txn = InventoryTransaction(
            product_id=product_id,
            transaction_type=txn_type,
            quantity_changed=quantity,
            transaction_date=datetime.utcnow().date(),  # match DATE column
            notes=notes
        )

        db.session.add(txn)

        product = Product.query.get(product_id)
        product.quantity_in_stock += quantity

        db.session.commit()
        flash('Transaction recorded successfully!')
        return redirect(url_for('view_transactions'))

    return render_template('add_transaction.html', products=products)

# ---------- Reports ----------
@app.route('/reports')
def view_reports():
    order_details = OrderDetail.query.all()
    return render_template('reports.html', order_details=order_details)

@app.route('/dashboard')
def dashboard():
    total_products = Product.query.count()
    total_suppliers = Supplier.query.count()
    total_orders = Order.query.count()
    low_stock_count = Product.query.filter(Product.quantity_in_stock < 10).count()

    return render_template(
        'dashboard.html',
        total_products=total_products,
        total_suppliers=total_suppliers,
        total_orders=total_orders,
        low_stock_count=low_stock_count
    )



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
