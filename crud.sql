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


SELECT 
    o.order_id,
    o.order_date,
    s.name AS supplier_name,
    p.name AS product_name,
    od.quantity,
    od.unit_price,
    (od.quantity * od.unit_price) AS total_price
FROM Orders o
JOIN OrderDetails od ON o.order_id = od.order_id
JOIN Products p ON od.product_id = p.product_id
JOIN Suppliers s ON o.supplier_id = s.supplier_id
ORDER BY o.order_date DESC;

SELECT 
    p.name AS product_name,
    SUM(od.quantity) AS total_quantity_ordered
FROM OrderDetails od
JOIN Products p ON od.product_id = p.product_id
GROUP BY p.name
ORDER BY total_quantity_ordered DESC;


SELECT 
    product_id,
    name,
    quantity_in_stock
FROM Products
WHERE quantity_in_stock < 10;

ALTER TABLE InventoryTransactions
ADD COLUMN product_name VARCHAR(100);

UPDATE InventoryTransactions t
JOIN Products p ON t.product_id = p.product_id
SET t.product_name = p.name
WHERE t.product_name IS NULL;

UPDATE OrderDetails d
JOIN Products p ON d.product_id = p.product_id
SET d.product_name = p.name
WHERE d.product_name IS NULL;
