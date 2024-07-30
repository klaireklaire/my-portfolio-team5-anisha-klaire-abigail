from flask import Flask, render_template,request, jsonify, send_from_directory
from getData import portfolio_df

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

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    #portfolio_subset = portfolio_df['Stock Ticker', 'Company Name', 'Current Price', 'Change in Price %', 'Number of Shares', 'Total Value']
    table_html = portfolio_df.to_html(classes='table table-striped', index=False)
    return render_template('index1.html', table_html=table_html)
    


if __name__ == '__main__':
    app.run(debug=True)
