import os

def model(dbt, session):
    dbt.config(
        materialized="incremental",
        tags=["python", "dml_sample"],
        unique_key="id"
    )
    target_table = dbt.this
    file_path = os.path.join(os.path.dirname(__file__), "sql_statements.sql")
    with open(file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    sql_content = sql_content.format(target_table=target_table)
    sql_statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
    for stmt in sql_statements:
        session.sql(stmt).collect()
    return session.table(target_table)
