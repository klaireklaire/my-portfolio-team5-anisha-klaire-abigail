from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
