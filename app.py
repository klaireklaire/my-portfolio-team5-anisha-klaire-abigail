from flask import Flask, render_template, request, send_file
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
     # Get the stock ticker from the request
    ticker = request.args.get('ticker')
    range_option = request.args.get('range', '1y')
    
    if not ticker:
        return "No ticker provided", 400

    # Define the date range based on the selected option
    end_date = datetime.now()
    if range_option == '1y':
        start_date = end_date - timedelta(days=365)
        title_range = "1 Year"
    elif range_option == '6m':
        start_date = end_date - timedelta(days=182)
        title_range = "6 Months"
    elif range_option == '3m':
        start_date = end_date - timedelta(days=91)
        title_range = "3 Months"
    elif range_option == '1m':
        start_date = end_date - timedelta(days=30)
        title_range = "1 Month"
    else:
        start_date = end_date - timedelta(days=365)
        title_range = "1 Year"  # Default to 1 year

    start_date = int(start_date.timestamp())
    end_date = int(end_date.timestamp())

    # Fetch the stock data
    df = pd.read_csv(
        f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true",
        parse_dates=['Date'],
        index_col='Date'
    )

    # Generate the plot
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Adj Close'], label='Adj Close Price')
    plt.title(f'{ticker} Stock Price Over the Last {title_range}')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price')
    plt.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
