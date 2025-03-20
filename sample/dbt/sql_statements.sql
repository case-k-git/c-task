INSERT INTO {target_table}
SELECT id, col1, current_timestamp() as updated_at
FROM stg_new_data
WHERE id NOT IN (SELECT id FROM {target_table});

UPDATE {target_table}
SET col1 = nd.col1,
    updated_at = current_timestamp()
FROM stg_new_data nd
WHERE {target_table}.id = nd.id;
