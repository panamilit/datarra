SELECT
    file_id,
    original_name,
    file_type,
    file_size,
    row_count,
    column_count,
    columns_json,
    uploaded_at
FROM datasets
ORDER BY uploaded_at DESC;