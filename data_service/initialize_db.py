#!/usr/bin/env python

"""initialize_db.py: Initialize MySQL database."""

<<<<<<< HEAD
import sqlite3

conn = sqlite3.connect("myPortfolio.sqlite")

cursor = conn.cursor()
sql_query="""   CREATE TABLE myPortfolio(
    stock_ticker TEXT NOT NULL,
    company_name TEXT NOT NULL,
    current_price REAL NOT NULL,
    change_in_price REAL,
    change_in_price_percent REAL,
    fifty_two_week_low REAL,
    fifty_two_week_high REAL,
    date_added TEXT,
    number_of_shares INTEGER,
    total_value REAL
    PRIMARY KEY(stock_ticker)
)"""
=======
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
            price DECIMAL(10, 2) NOT NULL,
            position INT NOT NULL,
            pl DECIMAL(10, 2) NOT NULL
        );
    """)
    # Insert sample data
    sample_data = [
        ('2023-01-01', 'AAPL', 'buy', 10, 150.00, 10, 0.00),
        ('2023-02-01', 'GOOG', 'buy', 5, 1000.00, 5, 0.00),
        ('2023-03-01', 'MSFT', 'sell', 8, 200.00, -8, 400.00),
        ('2023-04-01', 'TSLA', 'buy', 3, 600.00, 3, 0.00),
        ('2023-05-01', 'AMZN', 'sell', 2, 3000.00, -2, 6000.00)
    ]
    cursor.executemany("""
        INSERT INTO transactions (date, ticker, side, size, price, position, pl)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, sample_data)
    db.commit()
    cursor.close()
    db.close()
>>>>>>> origin/main
