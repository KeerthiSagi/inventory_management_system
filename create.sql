-- PRODUCTS TABLE
-- Functional Dependencies: product_id → name, description, price, quantity_in_stock
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    quantity_in_stock INT NOT NULL
);

-- SUPPLIERS TABLE
-- Functional Dependencies: supplier_id → name, contact_info, address
CREATE TABLE Suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100),
    address VARCHAR(255)
);

-- ORDERS TABLE
-- Functional Dependencies: order_id → order_date, supplier_id
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- ORDERDETAILS TABLE
-- Functional Dependencies: detail_id → order_id, product_id, quantity, unit_price
CREATE TABLE OrderDetails (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- INVENTORYTRANSACTIONS TABLE
-- Functional Dependencies: transaction_id → product_id, transaction_type, quantity_changed, transaction_date, notes
CREATE TABLE InventoryTransactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    transaction_type ENUM('IN', 'OUT') NOT NULL,
    quantity_changed INT NOT NULL,
    transaction_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);



select * from inventorytransactions;
select * from orderdetails; 
select * from orders;
select * from products;
select * from suppliers;
