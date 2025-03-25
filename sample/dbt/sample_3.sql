DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INT,
    product_name STRING,
    list_price DECIMAL(10,2)
);

INSERT INTO products (product_id, product_name, list_price) VALUES
    (1, 'Laptop', 1200.00),
    (2, 'Smartphone', 800.00),
    (3, 'Tablet', 600.00),
    (4, 'Headphones', 150.00),
    (5, 'Monitor', 300.00);

