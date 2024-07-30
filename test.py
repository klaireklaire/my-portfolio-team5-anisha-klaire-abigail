import time
from datetime import datetime
import pandas as pd

dt = datetime(2024, 7, 25)
start_date = int(round(dt.timestamp()))

dt = datetime(2024, 7, 26)
end_date = int(round(dt.timestamp()))

stock = 'GOOG'

df = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true",
    parse_dates = ['Date'], index_col='Date')

print(df)

import yfinance as yf

msft = yf.Ticker("MSFT")

# get all stock info
print(msft.info)