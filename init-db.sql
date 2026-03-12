-- Create disease_detection database if it doesn't exist
-- Note: postgres container creates it automatically via POSTGRES_DB env var
-- This script just ensures the table exists

CREATE TABLE IF NOT EXISTS disease_prediction (
    id VARCHAR(36) PRIMARY KEY,
    image_path VARCHAR(255) NOT NULL,
    prediction_detail VARCHAR(255) NOT NULL,
    healthy BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on creation timestamp for faster queries
CREATE INDEX IF NOT EXISTS idx_disease_prediction_created_at ON disease_prediction(created_at);
