def model(dbt, session):
    dbt.config(
        materialized="incremental",
        tags=["python", "dml_sample"],
        unique_key="id"
    )
    
    target_table = dbt.this
    df_new = dbt.ref("stg_new_data")
    
    session.sql(f"""
        INSERT INTO {target_table}
        SELECT id, col1, current_timestamp() as updated_at
        FROM stg_new_data
        WHERE id NOT IN (SELECT id FROM {target_table})
    """).collect()
    
    session.sql(f"""
        UPDATE {target_table}
        SET col1 = nd.col1,
            updated_at = current_timestamp()
        FROM stg_new_data nd
        WHERE {target_table}.id = nd.id
    """).collect()
    
    return session.table(target_table)
