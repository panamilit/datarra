INSERT INTO users (
    email,
    password_hash,
    display_name,
    auth_provider
)
VALUES (%s, %s, %s, 'local')
RETURNING id, email, display_name, auth_provider, is_admin, created_at;