-- DUMMY
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id INT,
    otll INT,
    product_name STRING,
    quantity INT,
    order_date DATE
);

INSERT INTO orders (order_id, otll, product_name, quantity, order_date)
VALUES
    (1,  50000,  'Item A', 10, '2023-01-01'),
    (2, 150000,  'Item B',  5, '2023-02-01'),
    (3, 250000,  'Item C',  3, '2023-03-01');

DROP TABLE IF EXISTS small_orders;
CREATE TABLE small_orders (
    order_id INT,
    otll INT,
    product_name STRING,
    quantity INT,
    order_date DATE
);

DROP TABLE IF EXISTS medium_orders;
CREATE TABLE medium_orders (
    order_id INT,
    otll INT,
    product_name STRING,
    quantity INT,
    order_date DATE
);

DROP TABLE IF EXISTS large_orders;
CREATE TABLE large_orders (
    order_id INT,
    otll INT,
    product_name STRING,
    quantity INT,
    order_date DATE
);

-- DML
CREATE TEMPORARY VIEW orders_source AS
SELECT
    struct(*) AS data,
    CASE
        WHEN otll < 100000 THEN 'small_orders'
        WHEN otll >= 100000 AND otll < 200000 THEN 'medium_orders'
        WHEN otll >= 200000 THEN 'special_orders'
    END AS target
FROM orders;

INSERT INTO small_orders
SELECT data.*
FROM orders_source
WHERE target = 'small_orders';

INSERT INTO medium_orders
SELECT data.*
FROM orders_source
WHERE target = 'medium_orders';

INSERT INTO large_orders
SELECT data.*
FROM orders_source
WHERE target = 'special_orders';

