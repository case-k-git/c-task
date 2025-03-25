c_product = spark.sql(f"""
SELECT
  product_name,
  list_price
FROM products
ORDER BY
  list_price DESC
""")

for r_product in c_product.take(1000):
    print(r_product["product_name"] + " : $" + r_product["list_price"])
