#!/usr/bin/env python

"""app.py: Set up app routes and API endpoints for the app."""

from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import data_service.initialize_db as db_service
from data_service.getData import portfolio_df
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database connection details
def create_db_connection(db_name=None):
    return mysql.connector.connect(
        host=os.getenv("FLASK_DB_HOST"),
        user=os.getenv("FLASK_DB_USER"),
        password=os.getenv("FLASK_DB_PASSWORD"),
        database=db_name or os.getenv("FLASK_DB_NAME")
    )

@app.route('/')
def home():
    # Convert portfolio DataFrame to HTML table
    table_html = portfolio_df.to_html(classes='table table-striped', index=False)
    return render_template('index.html', portfolio_html=table_html)

@app.route('/chart_data')
def chart_data():
    ticker = request.args.get('ticker')
    range_option = request.args.get('range', '1y')
    
    if not ticker:
        return jsonify({'error': 'No ticker provided'}), 400

    end_date = datetime.now()
    if range_option == '1y':
        start_date = end_date - timedelta(days=365)
    elif range_option == '6m':
        start_date = end_date - timedelta(days=182)
    elif range_option == '3m':
        start_date = end_date - timedelta(days=91)
    elif range_option == '1m':
        start_date = end_date - timedelta(days=30)
    else:
        start_date = end_date - timedelta(days=365)  # Default to 1 year

    # Fetch the stock data
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)

    # Prepare data for Chart.js
    chart_data = {
        'labels': df.index.strftime('%Y-%m-%d').tolist(),
        'prices': df['Close'].tolist()
    }

    return jsonify(chart_data=chart_data)

@app.route('/additional_info')
def additional_info():
    ticker = request.args.get('ticker')
    
    if not ticker:
        return jsonify({'error': 'No ticker provided'}), 400

    stock = yf.Ticker(ticker)
    info = stock.info
    additional_info = {
        'open': info.get('open', 'N/A'),
        'high': info.get('dayHigh', 'N/A'),
        'low': info.get('dayLow', 'N/A'),
        'volume': info.get('volume', 'N/A'),
        'marketCap': info.get('marketCap', 'N/A'),
        'peRatio': info.get('trailingPE', 'N/A'),
        '52WeekHigh': info.get('fiftyTwoWeekHigh', 'N/A'),
        '52WeekLow': info.get('fiftyTwoWeekLow', 'N/A'),
        'avgVolume': info.get('averageVolume', 'N/A'),
        'yield': info.get('dividendYield', 'N/A'),
        'beta': info.get('beta', 'N/A'),
        'eps': info.get('trailingEps', 'N/A')
    }

    return jsonify(additional_info=additional_info)
    

@app.route('/transactions', methods=['GET'])
def get_transactions():
    db = create_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(transactions)

@app.route('/transactions', methods=['POST'])
def add_transaction():
    db = create_db_connection()
    cursor = db.cursor()
    data = request.json
    query = """
        INSERT INTO transactions (date, ticker, side, size, price, position, pl)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (data['date'], data['ticker'], data['side'], data['size'], data['price'], data['position'], data['pl']))
    db.commit()
    transaction_id = cursor.lastrowid
    cursor.close()
    db.close()
    return jsonify({'id': transaction_id}), 201

@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    db = create_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
    transaction = cursor.fetchone()
    cursor.close()
    db.close()
    if transaction:
        return jsonify(transaction)
    else:
        return jsonify({'error': 'Transaction not found'}), 404

def calculate_position():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT ticker, position, side FROM transactions"
    cursor.execute(query)
    transactions = cursor.fetchall()
    cursor.close()
    connection.close()
    
    portfolio={}
    for t in transactions:
        ticker = t['ticker']
        quantity = t['position']
        side = t['side']
        
        if ticker not in portfolio:
            portfolio[ticker] = 0
        
        if side =='buy':
            portfolio[ticker] += quantity
        elif side =='sell':
            portfolio[ticker] -= quantity
        
    return portfolio

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    
    portfolio = calculate_position()
    return jsonify(portfolio)


    
    

if __name__ == '__main__':
    db_service.initialize_database()  # Initialize the database tables
    app.run(debug=True)
