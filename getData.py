import yfinance as yf
import pandas as pd

# List of ticker symbols
ticker_symbols = ["AAPL", "AMZN", "TSLA", "META", "MSFT"]

stock_data=[]

# Fetch the current price for each ticker
for ticker in ticker_symbols:
    ticker_data = yf.Ticker(ticker)

    current_price_stock = ticker_data.info['currentPrice']
    price_change_stock = ticker_data.info['currentPrice'] - ticker_data.info['previousClose']
    price_change_percentage_stock = ticker_data.info['currentPrice']/ticker_data.info['previousClose']-1
    fifty_two_week_low = ticker_data.info['fiftyTwoWeekLow']
    fifty_two_week_high = ticker_data.info['fiftyTwoWeekHigh']
    stock_data.append({
        'Stock Ticker': ticker,
        'Company Name': ticker_data.info['shortName'],
        'Current Price': current_price_stock,
        'Change in Price': price_change_stock,
        'Change in Price %': price_change_percentage_stock,
        '52-Week Low': fifty_two_week_low,
        '52-Week High': fifty_two_week_high
    }    
    )

print(stock_data)

columns = ['Stock Ticker', 'Company Name', 'Current Price', 'Change in Price', 'Change in Price %', '52-Week Low', '52-Week High']

portfolio_df = pd.DataFrame(stock_data, columns=columns)
print(portfolio_df)