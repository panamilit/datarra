/* TABLE: datasets  */

CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    file_id UUID NOT NULL UNIQUE,
    original_name VARCHAR(255) NOT NULL,
    stored_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE datasets
ADD COLUMN row_count INTEGER,
ADD COLUMN column_count INTEGER,
ADD COLUMN columns_json JSONB;



ALTER TABLE datasets
ADD COLUMN user_id INTEGER REFERENCES users(id);


/* TABLE: users  */

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT,
    auth_provider VARCHAR(50) DEFAULT 'local',
    google_id VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);