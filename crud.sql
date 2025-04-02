-- CREATE: Add a new product
INSERT INTO Products (name, description, price, quantity_in_stock)
VALUES ('Smartwatch', 'Touchscreen fitness tracker', 120.00, 12);

-- READ: View all products under $100
SELECT * FROM Products
WHERE price < 100;

-- UPDATE: Increase stock of a specific product
UPDATE Products
SET quantity_in_stock = quantity_in_stock + 10
WHERE name = 'Keyboard';

-- CREATE: Create a new order and details
INSERT INTO Orders (order_date, supplier_id)
VALUES ('2025-03-12', 3);

INSERT INTO OrderDetails (order_id, product_id, quantity, unit_price)
VALUES (11, 1, 2, 820.00);

-- READ: Show order summary with supplier name
SELECT o.order_id, o.order_date, s.name AS supplier_name
FROM Orders o
JOIN Suppliers s ON o.supplier_id = s.supplier_id
WHERE o.order_id = 11;

-- DELETE: Remove a product by ID
DELETE FROM Products
WHERE product_id = 11;
