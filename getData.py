import yfinance as yf

# List of ticker symbols
ticker_symbols = ["AAPL", "AMZN", "TSLA", "MSFT"]

# List to store current prices
current_prices = []

# Fetch the current price for each ticker
for ticker in ticker_symbols:
    ticker_data = yf.Ticker(ticker)
    current_price = ticker_data.info['currentPrice']
    current_prices.append(current_price)

# Print the prices in order
for ticker, price in zip(ticker_symbols, current_prices):
    print(f"The current price of {ticker} is ${price:.2f}")
