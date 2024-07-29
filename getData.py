# import yfinance as yf

# # List of ticker symbols
# ticker_symbols = ["AAPL", "AMZN", "TSLA", "FB", "MSFT"]

# # List to store current prices
# current_prices = []

# # Fetch the current price for each ticker
# for ticker in ticker_symbols:
#     ticker_data = yf.Ticker(ticker)
#     current_price = ticker_data.info['currentPrice']
#     current_prices.append(current_price)

# # Print the prices in order
# for ticker, price in zip(ticker_symbols, current_prices):
#     print(f"The current price of {ticker} is ${price:.2f}")

import yfinance as yf

# Define the ticker symbol
ticker_symbol = "AAPL"

# Get data on this ticker
ticker_data = yf.Ticker(ticker_symbol)

# Get the current price
current_price = ticker_data.info['currentPrice']

print(f"The current price of {ticker_symbol} is ${current_price:.2f}")