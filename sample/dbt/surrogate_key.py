from pyspark.sql import functions as F

# 対象のテーブル名を指定
table_name = "your_table"

columns_df = spark.sql(f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position
""")
candidate_columns = [row["column_name"] for row in columns_df.collect()]

df = spark.table(table_name)

total_count = df.count()
selected_columns = []
for col in candidate_columns:
    selected_columns.append(col)
    distinct_count = df.select(*selected_columns).distinct().count()
    print(f"Unique count for candidate columns {selected_columns}: {distinct_count}")
    if distinct_count == total_count:
        break

print("Columns used for surrogate key:", selected_columns)

df_with_key = df.withColumn(
    "surrogate_key",
    F.sha2(F.concat_ws("-", *[F.col(c) for c in selected_columns]), 256)
)

df_with_key.show(truncate=False)
