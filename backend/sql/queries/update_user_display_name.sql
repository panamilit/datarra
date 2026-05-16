UPDATE users
SET display_name = %s
WHERE id = %s
RETURNING id, email, display_name, is_admin, created_at;