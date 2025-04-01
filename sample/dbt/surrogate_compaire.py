from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

# Create a SparkSession (or use an existing one)
spark = SparkSession.builder.appName("DifferenceCheck").getOrCreate()

# Load the tables "TableA" and "TableB" from the Hive metastore (or other sources)
table_name = "TableA"

dfA = spark.table(table_name)
dfB = spark.table("TableB")

# Define a function to extract differences for a specific column
def get_diff(dfA, dfB, key, column):
    # Join on the common key
    joined_df = dfA.alias("a").join(dfB.alias("b"), col("a." + key) == col("b." + key))
    # Filter rows where the values differ (including NULL checks)
    diff_df = joined_df.filter(
        (col("a." + column) != col("b." + column)) |
        (col("a." + column).isNull() & col("b." + column).isNotNull()) |
        (col("a." + column).isNotNull() & col("b." + column).isNull())
    ).select(
        col("a." + key).alias(key),
        lit(column).alias("column_name"),
        col("a." + column).alias("tableA_value"),
        col("b." + column).alias("tableB_value")
    )
    return diff_df

# List of columns to compare
# columns = ["col1", "col2"]
columns_df = spark.sql(f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position
""")
# Create a list of candidate columns for surrogate key generation
columns = [row["column_name"] for row in columns_df.collect()]

# Extract differences for each column and combine them into one DataFrame
diffs = None
for col_name in columns:
    diff = get_diff(dfA, dfB, "id", col_name)
    diffs = diff if diffs is None else diffs.union(diff)

# Display the differences
diffs.show()

# Save the results as a table named "differences" (using overwrite mode)
diffs.write.mode("overwrite").saveAsTable("differences")
