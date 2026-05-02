-- ============================================
-- PostgreSQL Setup Script
-- Project: Real-Time E-Commerce Events Pipeline
-- ============================================

-- Create database
CREATE DATABASE events_db;

-- Connect to the database
\c events_db;

-- Drop table for clean re-run during development
DROP TABLE IF EXISTS user_events;

-- Create table
CREATE TABLE user_events (
    event_id UUID PRIMARY KEY,  
    user_id INT NOT NULL,
    event_type VARCHAR(20) NOT NULL CHECK (event_type IN ('view','purchase')),
    product_id INT NOT NULL,
    product_name VARCHAR(255),
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    event_timestamp TIMESTAMP NOT NULL,  
    event_hour INT  
);

-- Indexes for query performance
CREATE INDEX idx_event_timestamp ON user_events(event_timestamp);
CREATE INDEX idx_event_type ON user_events(event_type);
CREATE INDEX idx_user ON user_events(user_id);

-- Composite indexes for frequent analytical queries
CREATE INDEX idx_user_time ON user_events(user_id, event_timestamp);
CREATE INDEX idx_event_type_time ON user_events(event_type, event_timestamp);