DELETE FROM datasets
WHERE file_id = %s
RETURNING file_path;