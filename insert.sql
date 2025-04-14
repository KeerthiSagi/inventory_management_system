-- PRODUCTS
INSERT INTO Products (name, description, price, quantity_in_stock) VALUES
('Laptop', '14-inch business laptop', 850.00, 10),
('Wireless Mouse', 'Ergonomic mouse with USB receiver', 25.50, 50),
('Keyboard', 'Mechanical keyboard with backlight', 45.00, 30),
('Monitor', '24-inch FHD monitor', 150.00, 20),
('Headphones', 'Noise-canceling headphones', 120.00, 25),
('Webcam', 'HD 1080p webcam with mic', 60.00, 15),
('Printer', 'Wireless inkjet printer', 200.00, 10),
('External HDD', '1TB USB 3.0 external drive', 75.00, 18),
('USB Hub', '4-port USB 3.0 hub', 20.00, 40),
('Desk Lamp', 'LED desk lamp with brightness control', 35.00, 22);

-- SUPPLIERS
INSERT INTO Suppliers (name, contact_info, address) VALUES
('Tech Supplies Inc.', 'tech@supplies.com', '123 Silicon Ave, NY'),
('Gadget World', 'contact@gadgetworld.com', '456 Innovation Blvd, SF'),
('Digital Gear', 'sales@digitalgear.com', '789 Cloud St, Seattle'),
('Nova Tech', 'support@novatech.com', '1010 Binary Way, Austin'),
('Office Depot', 'info@officedepot.com', '111 Paper Ln, Chicago'),
('Bytes & Bits', 'hello@bytesnbits.com', '222 Tech Dr, Boston'),
('MegaComp', 'sales@megacomp.com', '333 Compute Cir, Dallas'),
('NextGen Devices', 'ng@nextgen.com', '444 Chip Row, Houston'),
('ProWare', 'service@proware.com', '555 Logic Ave, Denver'),
('Micro Center', 'contact@microcenter.com', '666 Silicon Blvd, LA');

-- ORDERS
INSERT INTO Orders (order_date, supplier_id) VALUES
('2025-03-01', 1),
('2025-03-02', 2),
('2025-03-03', 3),
('2025-03-04', 4),
('2025-03-05', 5),
('2025-03-06', 6),
('2025-03-07', 7),
('2025-03-08', 8),
('2025-03-09', 9),
('2025-03-10', 10);

-- ORDERDETAILS
INSERT INTO OrderDetails (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 5, 830.00),
(2, 2, 10, 24.00),
(3, 3, 8, 43.00),
(4, 4, 6, 145.00),
(5, 5, 7, 115.00),
(6, 6, 4, 58.00),
(7, 7, 2, 195.00),
(8, 8, 5, 70.00),
(9, 9, 12, 18.00),
(10, 10, 3, 30.00);

-- INVENTORYTRANSACTIONS
INSERT INTO InventoryTransactions (product_id, transaction_type, quantity_changed, transaction_date, notes) VALUES
(1, 'IN', 5, '2025-03-01', 'Initial stock load'),
(2, 'IN', 10, '2025-03-02', 'Bulk stock added'),
(3, 'IN', 8, '2025-03-03', 'Reorder from supplier'),
(4, 'IN', 6, '2025-03-04', 'Inventory refresh'),
(5, 'OUT', 2, '2025-03-05', 'Customer purchase'),
(6, 'IN', 4, '2025-03-06', 'New arrival'),
(7, 'OUT', 1, '2025-03-07', 'Sample dispatch'),
(8, 'OUT', 3, '2025-03-08', 'Order shipment'),
(9, 'IN', 12, '2025-03-09', 'Stock top-up'),
(10, 'OUT', 3, '2025-03-10', 'Returned units sold');



-- Clean Insert Script for Inventory Management System

INSERT INTO Suppliers (name, contact_info, address) VALUES
('Digital Gear', 'support@digitalgear.com', '123 Tech Street, San Jose, CA'),
('OfficeWorld', 'hello@officeworld.com', '456 Office Blvd, Austin, TX'),
('ProSupply', 'sales@prosupply.com', '789 Supply Lane, Chicago, IL');

INSERT INTO Products (name, description, price, quantity_in_stock) VALUES
('Wireless Mouse', 'Ergonomic mouse with USB receiver', 25.50, 50),
('Mechanical Keyboard', 'RGB backlit mechanical keyboard', 45.00, 40),
('Laptop Stand', 'Aluminum adjustable laptop stand', 30.00, 30),
('USB Hub', '4-port USB 3.0 hub', 15.00, 25),
('Webcam', 'HD webcam with microphone', 60.00, 15);

INSERT INTO Orders (supplier_id, order_date) VALUES
(1, '2024-04-01'),
(2, '2024-04-02'),
(3, '2024-04-03');

INSERT INTO OrderDetails (order_id, product_id, product_name, quantity, unit_price) VALUES
(1, 1, 'Wireless Mouse', 10, 25.50),
(1, 2, 'Mechanical Keyboard', 5, 45.00),
(2, 3, 'Laptop Stand', 8, 30.00),
(2, 4, 'USB Hub', 4, 15.00),
(3, 5, 'Webcam', 3, 60.00);

INSERT INTO InventoryTransactions (
  product_id, product_name, transaction_type, quantity_changed, transaction_date, notes
) VALUES
(1, 'Wireless Mouse', 'IN', 10, '2024-04-01', 'Restocked from Digital Gear'),
(2, 'Mechanical Keyboard', 'IN', 5, '2024-04-01', 'Restocked from Digital Gear'),
(3, 'Laptop Stand', 'IN', 8, '2024-04-02', 'Restocked from OfficeWorld'),
(4, 'USB Hub', 'IN', 4, '2024-04-02', 'Restocked from OfficeWorld'),
(5, 'Webcam', 'IN', 3, '2024-04-03', 'Restocked from ProSupply'),
(1, 'Wireless Mouse', 'OUT', -10, '2024-04-04', 'Auto-OUT for Order #1'),
(2, 'Mechanical Keyboard', 'OUT', -5, '2024-04-04', 'Auto-OUT for Order #1'),
(3, 'Laptop Stand', 'OUT', -8, '2024-04-05', 'Auto-OUT for Order #2'),
(4, 'USB Hub', 'OUT', -4, '2024-04-05', 'Auto-OUT for Order #2'),
(5, 'Webcam', 'OUT', -3, '2024-04-06', 'Auto-OUT for Order #3');