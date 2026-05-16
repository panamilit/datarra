SELECT
    file_id,
    original_name,
    stored_name,
    file_path,
    file_type,
    file_size,
    row_count,
    column_count,
    columns_json,
    uploaded_at
FROM datasets
WHERE file_id = %s AND user_id = %s;