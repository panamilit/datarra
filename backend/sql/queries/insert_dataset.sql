INSERT INTO datasets (
    file_id,
    original_name,
    stored_name,
    file_path,
    file_type,
    file_size,
    row_count,
    column_count,
    columns_json,
    user_id
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
RETURNING id;