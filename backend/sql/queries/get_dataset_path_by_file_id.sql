SELECT
    file_path,
    file_type
FROM datasets
WHERE file_id = %s
AND user_id = %s;