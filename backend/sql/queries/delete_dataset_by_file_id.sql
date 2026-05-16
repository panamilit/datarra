DELETE FROM datasets
WHERE file_id = %s AND user_id = %s
RETURNING file_path;