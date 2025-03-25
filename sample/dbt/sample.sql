MERGE INTO bonuses D
USING (
    SELECT employee_id, salary, department_id
    FROM employees
    WHERE department_id = 80
) S
ON (D.employee_id = S.employee_id)
WHEN MATCHED AND (S.salary > 8000) THEN
    DELETE
WHEN MATCHED THEN
    UPDATE
        SET D.bonus = D.bonus + S.salary * 0.02
WHEN NOT MATCHED AND (S.salary <= 8000) THEN
    INSERT (D.employee_id, D.bonus)
    VALUES (S.employee_id, S.salary * 0.01);

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

# block 1
# PL/SQL cursor for LOOP example
c_product = spark.sql(f"""
SELECT
  product_name,
  list_price
FROM products
ORDER BY
  list_price DESC
""")

for r_product in c_product.take(1000):
    # FIXME databricks.migration.task Review and Update default max records limit (1000)
    # s_e_t to above df.api call to avoid collecting large number of records to driver
    print(r_product["product_name"] + " : $" + r_product["list_price"])
