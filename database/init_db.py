#!/usr/bin/env python3
"""
Database initialization script for Scopira
"""

import os
import sys
import psycopg2
from psycopg2 import sql

# Add parent directory to path to import backend modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def create_database():
    """Create the Scopira database"""
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgres',
        'dbname': 'postgres'  # Connect to default database first
    }
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create the scopira database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier('scopira')
        ))
        
        print("Database 'scopira' created successfully")
        
        # Close connection
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

def create_tables():
    """Create tables in the Scopira database"""
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgres',
        'dbname': 'scopira'
    }
    
    try:
        # Connect to Scopira database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        cursor.execute(schema_sql)
        conn.commit()
        
        print("Tables created successfully")
        
        # Close connection
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        return False
    except FileNotFoundError:
        print(f"Schema file not found: {schema_path}")
        return False
    
    return True

def insert_sample_data():
    """Insert sample data for testing"""
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'postgres',
        'dbname': 'scopira'
    }
    
    try:
        # Connect to Scopira database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Insert sample users
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name) 
            VALUES 
            ('johndoe', 'john.doe@example.com', 'hashed_password_1', 'John', 'Doe'),
            ('janedoe', 'jane.doe@example.com', 'hashed_password_2', 'Jane', 'Doe')
        """)
        
        # Insert sample jobs
        cursor.execute("""
            INSERT INTO jobs (title, company, description, requirements, location, salary_range) 
            VALUES 
            ('Senior Data Scientist', 'TechCorp', 'Looking for experienced data scientist', 
             '["Python", "Machine Learning", "SQL"]', 'San Francisco, CA', '$120,000 - $150,000'),
            ('Machine Learning Engineer', 'AI Innovations', 'Develop ML models at scale', 
             '["Python", "TensorFlow", "AWS"]', 'New York, NY', '$110,000 - $140,000')
        """)
        
        conn.commit()
        print("Sample data inserted successfully")
        
        # Close connection
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error inserting sample data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Initializing Scopira database...")
    
    # Create database
    if create_database():
        # Create tables
        if create_tables():
            # Insert sample data
            insert_sample_data()
    
    print("Database initialization complete!")