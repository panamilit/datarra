SELECT
    id,
    email,
    password_hash,
    display_name,
    auth_provider,
    is_admin,
    created_at
FROM users
WHERE email = %s;