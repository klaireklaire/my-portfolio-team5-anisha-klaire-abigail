#!/usr/bin/env python

"""initialize_db.py: Initialize MySQL database and connect it with Python and Flask app."""

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
