from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Product, Supplier, Order, OrderDetail, InventoryTransaction
from datetime import datetime
from sqlalchemy import text

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
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        quantity = int(request.form['quantity_in_stock'])
        notes = request.form.get('notes', '')

        new_product = Product(
            name=name,
            description=description,
            price=price,
            quantity_in_stock=quantity
        )

        db.session.add(new_product)
        db.session.flush()
        
        if quantity > 0:
            txn = InventoryTransaction(
                product_id=new_product.product_id,
                transaction_type='IN',
                quantity_changed=quantity,
                transaction_date=datetime.utcnow().date(),
                notes=notes or "Initial stock for new product"
            )
            db.session.add(txn)

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
        order_note = request.form.get('order_note', '')
        db.session.add(order)
        db.session.flush()  # to get order_id before commit

        for product in products:
            qty = int(request.form.get(f'quantity_{product.product_id}', 0))
            price = float(request.form.get(f'price_{product.product_id}', 0.0))
            if qty > 0:
                if product.quantity_in_stock < qty:
                    flash(f"Not enough stock for {product.name}. Available: {product.quantity_in_stock}", 'danger')
                    return redirect(url_for('add_order'))

                detail = OrderDetail(order_id=order.order_id, product_id=product.product_id, quantity=qty, unit_price=price)
                db.session.add(detail)

                product.quantity_in_stock -= qty  # Subtracting stock for customer order

                txn = InventoryTransaction(
                    product_id=product.product_id,
                    transaction_type='OUT',
                    quantity_changed=-qty,
                    transaction_date=datetime.utcnow().date(),
                    notes=order_note or f"Auto-OUT for Order #{order.order_id}"
                )

                db.session.add(txn)
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

from sqlalchemy import func
from datetime import datetime, timedelta

@app.route('/report/most_ordered_products')
def most_ordered_products():
    results = db.session.execute(text('''
        SELECT p.name AS product_name, SUM(od.quantity) AS total_quantity
        FROM OrderDetails od
        JOIN Products p ON od.product_id = p.product_id
        GROUP BY p.name
        ORDER BY total_quantity DESC
    '''))
    return render_template('reports.html', report_title="Most Ordered Products", report_rows=results, headers=["Product Name", "Total Quantity"])


@app.route('/report/low_stock_products')
def low_stock_products():
    results = db.session.execute(text('''
        SELECT name, quantity_in_stock
        FROM Products
        WHERE quantity_in_stock < (
            SELECT AVG(quantity_in_stock) FROM Products
        )
    '''))
    return render_template('reports.html', report_title="Low Stock Products (Below Average)", report_rows=results, headers=["Product Name", "Stock"])

@app.route('/report/supplier_order_summary')
def supplier_order_summary():
    results = db.session.execute(text('''
        SELECT s.name AS supplier_name, COUNT(o.order_id) AS order_count, SUM(od.quantity) AS total_quantity
        FROM Suppliers s
        JOIN Orders o ON s.supplier_id = o.supplier_id
        JOIN OrderDetails od ON o.order_id = od.order_id
        GROUP BY s.name
        ORDER BY order_count DESC
    '''))
    return render_template('reports.html', report_title="Supplier Order Summary", report_rows=results, headers=["Supplier Name", "Orders", "Total Quantity"])

@app.route('/report/recent_orders')
def recent_orders():
    last_7_days = datetime.utcnow() - timedelta(days=7)
    results = db.session.execute(
    text('''
        SELECT o.order_id, s.name AS supplier_name, o.order_date, SUM(od.quantity * od.unit_price) AS total_amount
        FROM Orders o
        JOIN Suppliers s ON o.supplier_id = s.supplier_id
        JOIN OrderDetails od ON o.order_id = od.order_id
        WHERE o.order_date >= :date
        GROUP BY o.order_id, s.name, o.order_date
        ORDER BY o.order_date DESC
    '''),
    {"date": last_7_days} 
)
    return render_template('reports.html', report_title="Recent Orders (Last 7 Days)", report_rows=results, headers=["Order ID", "Supplier", "Date", "Total Amount"])

@app.route('/report/reorder_suggestions')
def reorder_suggestions():
    results = db.session.execute(text('''
        SELECT p.name, SUM(od.quantity) AS total_ordered, p.quantity_in_stock
        FROM OrderDetails od
        JOIN Products p ON od.product_id = p.product_id
        GROUP BY p.product_id
        HAVING total_ordered > 10 AND p.quantity_in_stock < 5
        ORDER BY total_ordered DESC
    '''))
    return render_template('reports.html', report_title="Reorder Suggestions", report_rows=results, headers=["Product Name", "Total Ordered", "Stock Left"])

@app.route('/restock_product', methods=['POST'])
def restock_product_inline():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    note = request.form.get('notes', '')

    product = Product.query.get_or_404(product_id)
    product.quantity_in_stock += quantity

    txn = InventoryTransaction(
        product_id=product_id,
        transaction_type='IN',
        quantity_changed=quantity,
        transaction_date=datetime.utcnow().date(),
        notes=note or "Restock via product page"
    )
    db.session.add(txn)
    db.session.commit()

    flash(f'{quantity} units added to {product.name}')
    return redirect(url_for('view_products'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
