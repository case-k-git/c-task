from pyspark.sql import functions as F
from pyspark.sql import Row

# List of input table names (replace with your actual table names)
table_names = ["your_table1", "your_table2", "your_table3"]

# List to store results for each table
results = []

# Process each table in the list
for table_name in table_names:
    # Retrieve column information for the table from information_schema.columns (ordered by ordinal position)
    columns_df = spark.sql(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position
    """)
    
    # Create a list of candidate columns for surrogate key generation
    candidate_columns = [row["column_name"] for row in columns_df.collect()]
    
    # Load the table into a DataFrame
    df = spark.table(table_name)
    
    # Get the total number of rows in the table
    total_count = df.count()
    
    # Dynamically select the minimal set of columns that uniquely identify each row
    selected_columns = []
    for col in candidate_columns:
        selected_columns.append(col)
        distinct_count = df.select(*selected_columns).distinct().count()
        print(f"Table {table_name} - Unique count for candidate columns {selected_columns}: {distinct_count}")
        if distinct_count == total_count:
            # Break if the current set of columns uniquely identifies every row
            break
    
    print("Table:", table_name, "-> Columns used for surrogate key:", selected_columns)
    
    # Append the result as a Row containing the table name and selected columns
    results.append(Row(table_name=table_name, selected_columns=selected_columns))

# Create a DataFrame from the results list and show the final output
result_df = spark.createDataFrame(results)
result_df.show(truncate=False)
