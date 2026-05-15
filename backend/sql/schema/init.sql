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