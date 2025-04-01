from pyspark.sql import functions as F

df = spark.table("your_table")

total_count = df.count()

candidate_columns = ["col1", "col2", "col3", "col4"]

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
