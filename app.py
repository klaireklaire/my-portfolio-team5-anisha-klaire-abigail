from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for Matplotlib
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    # Sample stock portfolio data
    portfolio = [
        {'ticker': 'AAPL', 'name': 'Apple Inc.', 'shares': 10, 'price': 150.00},
        {'ticker': 'GOOGL', 'name': 'Alphabet Inc.', 'shares': 5, 'price': 2800.00},
        {'ticker': 'TSLA', 'name': 'Tesla Inc.', 'shares': 8, 'price': 700.00},
    ]
    return render_template('index.html', portfolio=portfolio)

@app.route('/plot')
def plot():
    # Get the stock ticker and time range from the request
    ticker = request.args.get('ticker')
    range_option = request.args.get('range', '1y')
    
    if not ticker:
        return jsonify({'error': 'No ticker provided'}), 400

    # Define the date range based on the selected option
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

    start_date = int(start_date.timestamp())
    end_date = int(end_date.timestamp())

    # Fetch the stock data
    df = pd.read_csv(
        f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true",
        parse_dates=['Date'],
        index_col='Date'
    )

    # Prepare data for Chart.js
    data = {
        'labels': df.index.strftime('%Y-%m-%d').tolist(),
        'prices': df['Adj Close'].tolist()
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
