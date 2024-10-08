#!/usr/bin/env python

"""initialize_db.py: Initialize MySQL database."""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection details
def create_db_connection(db_name=None):
    return mysql.connector.connect(
        host=os.getenv("FLASK_DB_HOST"),
        user=os.getenv("FLASK_DB_USER"),
        password=os.getenv("FLASK_DB_PASSWORD"),
        database=db_name
    )

# Function to create the database
def create_database():
    try:
        db = create_db_connection()
        cursor = db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('FLASK_DB_NAME')}")
        cursor.close()
        db.close()
    except Error as e:
        print(f"Error creating database: {e}")

# Function to initialize the database
def initialize_database():
    create_database()
    db = create_db_connection(db_name=os.getenv('FLASK_DB_NAME'))
    cursor = db.cursor()
    # Drop existing tables if they exist and recreate them
    cursor.execute("DROP TABLE IF EXISTS transactions;")
    cursor.execute("""
        CREATE TABLE transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            ticker VARCHAR(10) NOT NULL,
            side ENUM('buy', 'sell') NOT NULL,
            size INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        );
    """)
    # Insert sample data
    sample_data = [
        ('2024-07-16', 'AAPL', 'buy', 10, 234.82),
        ('2024-03-06', 'GOOG', 'buy', 5, 132.56),
        ('2024-04-30', 'MSFT', 'buy', 6, 389.33),
        ('2024-03-12', 'TSLA', 'buy', 15, 177.54),
        ('2024-01-05', 'AMZN', 'buy', 10, 145.24)
    ]
    cursor.executemany("""
        INSERT INTO transactions (date, ticker, side, size, price)
        VALUES (%s, %s, %s, %s, %s)
    """, sample_data)
    db.commit()
    cursor.close()
    db.close()
