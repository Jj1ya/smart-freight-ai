-- database/schema.sql (PostgreSQL Version)

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,            -- AUTOINCREMENT -> SERIAL 변경
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Carriers Table
CREATE TABLE IF NOT EXISTS carriers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base_currency VARCHAR(3) DEFAULT 'USD',
    contact_email VARCHAR(100)
);

-- 3. Shipments Table
CREATE TABLE IF NOT EXISTS shipments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    origin_country VARCHAR(2) NOT NULL,
    dest_country VARCHAR(2) NOT NULL,
    weight_kg DECIMAL(10, 2) NOT NULL, -- REAL -> DECIMAL (더 정확함)
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- 4. Rates Table
CREATE TABLE IF NOT EXISTS rates (
    id SERIAL PRIMARY KEY,
    carrier_id INTEGER NOT NULL,
    origin_region VARCHAR(50) NOT NULL,
    dest_region VARCHAR(50) NOT NULL,
    rate_per_kg DECIMAL(10, 2) NOT NULL,
    effective_date DATE,
    FOREIGN KEY (carrier_id) REFERENCES carriers (id)
);