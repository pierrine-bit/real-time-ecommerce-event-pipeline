-- ============================================================
-- PostgreSQL Setup Script
-- Project: Real-Time E-Commerce Analytics Pipeline
-- ============================================================


-- Create database (run once)
CREATE DATABASE events_db;


-- Connect to database
\c events_db;


-- Drop table for development re-runs
DROP TABLE IF EXISTS fact_events;


-- Create analytics table
CREATE TABLE fact_events (

    event_id VARCHAR(36) PRIMARY KEY,

    session_id VARCHAR(36),

    user_id INT NOT NULL,

    event_type VARCHAR(20) NOT NULL
    CHECK (
        event_type IN (
            'view',
            'purchase'
        )
    ),

    product_id INT NOT NULL,

    product_name VARCHAR(100) NOT NULL,

    category VARCHAR(50),

    country VARCHAR(50),

    device_type VARCHAR(50),

    traffic_source VARCHAR(50),

    quantity INT NOT NULL
    CHECK (
        quantity > 0
    ),

    price NUMERIC(10,2) NOT NULL
    CHECK (
        price > 0
    ),

    discount NUMERIC(5,2)
    DEFAULT 0,

    revenue NUMERIC(12,2),

    event_timestamp TIMESTAMP NOT NULL,

    event_hour INT

);


-- ============================================================
-- Indexes for analytical queries
-- ============================================================


CREATE INDEX IF NOT EXISTS idx_fact_events_timestamp
ON fact_events(event_timestamp);


CREATE INDEX IF NOT EXISTS idx_fact_events_product
ON fact_events(product_id);


CREATE INDEX IF NOT EXISTS idx_fact_events_event_type
ON fact_events(event_type);


CREATE INDEX IF NOT EXISTS idx_fact_events_country
ON fact_events(country);


CREATE INDEX IF NOT EXISTS idx_fact_events_hour
ON fact_events(event_hour);


CREATE INDEX IF NOT EXISTS idx_fact_events_type_time
ON fact_events(
    event_type,
    event_timestamp
);