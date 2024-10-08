#!/usr/bin/env python

"""app.py: Set up app routes and API endpoints for the app."""

from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import data_service.initialize_db as db_service
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

portfolio_history = []

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
    portfolio = calculate_position()
    total_value = calculate_total_value(portfolio)
    return render_template('index.html', portfolio=portfolio, total_value=total_value)

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
        INSERT INTO transactions (date, ticker, side, size, price)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (data['date'], data['ticker'], data['side'], data['size'], data['price']))
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

@app.route('/buy', methods=['POST'])
def buy_stock():
    data = request.json
    ticker = data.get('ticker')
    size = data.get('size')
    
    if not ticker or not size:
        return jsonify({'error': 'Ticker and size are required'}), 400

    price = current_price(ticker)
    db = create_db_connection()
    cursor = db.cursor()
    query = """
        INSERT INTO transactions (date, ticker, side, size, price)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (datetime.now().date(), ticker, 'buy', size, price))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Stock bought successfully'}), 201

@app.route('/sell', methods=['POST'])
def sell_stock():
    data = request.json
    ticker = data.get('ticker')
    size = data.get('size')
    
    if not ticker or not size:
        return jsonify({'error': 'Ticker and size are required'}), 400

    portfolio = calculate_position()
    
    print(type(portfolio[ticker][0]), portfolio[ticker][0])
    print(type(size), size)
    
    if ticker not in portfolio or portfolio[ticker][0] < int(size):
        return jsonify({'error': 'Not enough shares to sell'}), 400

    price = current_price(ticker)
    db = create_db_connection()
    cursor = db.cursor()
    query = """
        INSERT INTO transactions (date, ticker, side, size, price)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (datetime.now().date(), ticker, 'sell', size, price))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'message': 'Stock sold successfully'}), 201

def current_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.info['currentPrice']

def percent_change(ticker):
    stock = yf.Ticker(ticker)
    price_change_percentage_stock = stock.info['currentPrice']/stock.info['previousClose']-1
    return price_change_percentage_stock

def calculate_position():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT ticker, size, side, price FROM transactions"
    cursor.execute(query)
    transactions = cursor.fetchall()
    cursor.close()
    connection.close()
    
    portfolio={} # key is the ticker and value []
    for t in transactions:
        ticker = t['ticker']
        quantity = t['size']
        side = t['side']
        price = t['price']
        
        if ticker not in portfolio:
            portfolio[ticker] = [0,price,0,0.0, 0.0,0.0] #intial average purchase price is the same as the buy price
        #if it is in portfolio and on the buy side then we need to calculate the average purchase price
        elif ticker in portfolio:
            if side == 'buy':
                # calculate the average purchase price
                portfolio[ticker][1] = (portfolio[ticker][1] * portfolio[ticker][0] + quantity * price) / (portfolio[ticker][0] + quantity)
        
        if side == 'buy':
            portfolio[ticker][0] += quantity
            portfolio[ticker][2] += price * quantity
        elif side == 'sell':
            portfolio[ticker][0] -= quantity
            
        portfolio[ticker][3]=current_price(ticker)
        portfolio[ticker][4]=Decimal(portfolio[ticker][3]*portfolio[ticker][0])-portfolio[ticker][2]
        portfolio[ticker][5]=percent_change(ticker)
    #portfolio be the stock ticker key and value as {total shares held[0],average purchase price[1], total cost basis[2], current value of 1 shares[3],
    # unrealized gain/loss[4], percent change in stock value}
    #I have the code for current price and unrealized gain/loss = current value - total cost basis
    #current value = current price *total amount of shares
    filtered_portfolio = {ticker: values for ticker, values in portfolio.items() if values[0] > 0}
    #only return if value>0
    return filtered_portfolio

def calculate_total_value(portfolio):
    total_value = sum(values[0]*values[3] for values in portfolio.values())
    return total_value

@app.route('/portfolio_history', methods=['GET'])
def get_portfolio_history():
    return jsonify(portfolio_history)

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    portfolio = calculate_position()
    total_value = calculate_total_value(portfolio)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append the current total value and timestamp to the history
    portfolio_history.append({'time': current_time, 'value': total_value})
    return jsonify(portfolio)

if __name__ == '__main__':
    db_service.initialize_database()  # Initialize the database tables
    app.run(debug=True)
