import yfinance as yf

# List of ticker symbols
ticker_symbols = ["AAPL", "AMZN", "TSLA", "META", "MSFT"]

# List to store current prices
current_prices = []
price_changes = []
price_changes_percentages = []


# Fetch the current price for each ticker
for ticker in ticker_symbols:
    ticker_data = yf.Ticker(ticker)

    current_price_stock = ticker_data.info['currentPrice']
    current_prices.append(current_price_stock)
    price_change_stock = ticker_data.info['currentPrice'] - ticker_data.info['previousClose']
    price_changes.append(price_change_stock)
    price_changes_percentage_stock = ticker_data.info['currentPrice']/ticker_data.info['previousClose']-1
    price_changes_percentages.append(price_changes_percentage_stock)


# Print the prices in order
for ticker, price in zip(ticker_symbols, current_prices):
    print(f"The current price of {ticker} is ${price:.2f}")

# Print the change in price in order
for ticker, change in zip(ticker_symbols, price_changes):
    print(f"The change in price of {ticker} is ${change:.2f}")

# Print the change percentage in order
for ticker, change_percent in zip(ticker_symbols, price_changes_percentages):
    print(f"The change in price percentage of {ticker} is {change_percent:.2f}%")



#thinking of what other data points are useful to us other than current prices
#Price Change: The change in price from the previous close, both in absolute terms 
# and as a percentage.

