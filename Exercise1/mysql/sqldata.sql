-- 1. Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(255),
    created_at DATETIME DEFAULT NOW()
);

INSERT INTO users (username, email, password)
VALUES 
('john_doe', 'john@example.com', 'pass123'),
('jane_smith', 'jane@example.com', 'pass456'),
('mike_jordan', 'mike@example.com', 'pass789'),
('sara_lee', 'sara@example.com', 'pass234'),
('chris_k', 'chris@example.com', 'pass345'),
('amy_wong', 'amy@example.com', 'pass987'),
('paul_b', 'paul@example.com', 'pass654'),
('nina_p', 'nina@example.com', 'pass321'),
('alex_r', 'alex@example.com', 'pass111'),
('linda_g', 'linda@example.com', 'pass222');

-- 2. Products Table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    stock INT
);

INSERT INTO products (name, description, price, stock)
VALUES 
('Laptop', '14-inch screen, 8GB RAM', 799.99, 20),
('Headphones', 'Noise-cancelling', 199.99, 50),
('Mouse', 'Wireless optical mouse', 29.99, 100),
('Keyboard', 'Mechanical RGB keyboard', 89.99, 30),
('Monitor', '24-inch Full HD', 149.99, 25),
('Tablet', '10-inch Android tablet', 299.99, 40),
('Smartwatch', 'Fitness tracking', 129.99, 35),
('Printer', 'All-in-one laser printer', 249.99, 15),
('Camera', 'DSLR with lens kit', 699.99, 10),
('Router', 'Dual-band WiFi router', 59.99, 60);

-- 3. Orders Table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATE,
    total DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO orders (user_id, order_date, total, status)
VALUES 
(1, '2024-04-01', 999.99, 'Shipped'),
(2, '2024-04-02', 129.99, 'Processing'),
(3, '2024-04-03', 49.99, 'Delivered'),
(4, '2024-04-04', 189.99, 'Cancelled'),
(5, '2024-04-05', 89.99, 'Shipped'),
(6, '2024-04-06', 159.99, 'Delivered'),
(7, '2024-04-07', 79.99, 'Returned'),
(8, '2024-04-08', 449.99, 'Processing'),
(9, '2024-04-09', 59.99, 'Shipped'),
(10, '2024-04-10', 129.99, 'Delivered');

-- 4. Order Items Table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES 
(1, 1, 1, 799.99),
(1, 2, 1, 199.99),
(2, 3, 2, 29.99),
(3, 4, 1, 89.99),
(4, 5, 1, 149.99),
(5, 6, 1, 299.99),
(6, 7, 1, 129.99),
(7, 8, 1, 249.99),
(8, 9, 1, 699.99),
(9, 10, 1, 59.99);

-- 5. Categories Table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
);

INSERT INTO categories (name, description)
VALUES 
('Electronics', 'Devices and gadgets'),
('Computers', 'Laptops, desktops and accessories'),
('Mobile', 'Smartphones and tablets'),
('Accessories', 'Mouse, keyboard, etc.'),
('Wearables', 'Smartwatches and fitness bands'),
('Networking', 'Routers and modems'),
('Cameras', 'Photography equipment'),
('Printing', 'Printers and cartridges'),
('Audio', 'Speakers and headphones'),
('Office', 'Office electronics');

-- 6. Product-Categories (Many-to-Many)
CREATE TABLE product_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    category_id INT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

INSERT INTO product_categories (product_id, category_id)
VALUES
(1, 2),
(2, 9),
(3, 4),
(4, 4),
(5, 2),
(6, 3),
(7, 5),
(8, 8),
(9, 7),
(10, 6);
