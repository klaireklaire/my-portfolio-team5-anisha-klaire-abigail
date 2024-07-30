from flask import Flask, render_template, request, jsonify
from getData import portfolio_df
from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
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

    start_date = int(start_date.timestamp())
    end_date = int(end_date.timestamp())

    # Fetch the stock data
    stock = yf.Ticker(ticker)
    df = stock.history(start=datetime.fromtimestamp(start_date), end=datetime.fromtimestamp(end_date))

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

if __name__ == '__main__':
    app.run(debug=True)
