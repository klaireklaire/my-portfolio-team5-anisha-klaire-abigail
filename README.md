<img width="1674" alt="image" src="https://github.com/user-attachments/assets/5407ab82-e9dd-4d30-8194-d4ce207c5e17">

### README.md

# InvestWise – Stock Portfolio Simulator

This project is a Stock Portfolio Simulator built using Flask, Python, and Bootstrap. It allows users to simulate stock trading, view stock performance, and manage a portfolio. 

## Features

- Simulate buying and selling stocks
- View stock performance charts
- Manage and track portfolio performance
- Display investment tips and strategies

## Prerequisites

- Python 3.x
- `pip` package manager
- MySQL Server activated and connected
- `python-dotenv` package

## Setup Instructions

### 1. Clone the Repository

```sh
git clone [https://github.com/your-repo/stock-portfolio-simulator.git](https://github.com/klaireklaire/my-portfolio-team5-anisha-klaire-abigail)
cd stock-portfolio-simulator
```

### 2. Set Up Environment Variables

To keep sensitive information such as database credentials secure and configurable, we use environment variables stored in a `.env` file.

#### Install `python-dotenv`

Make sure the `python-dotenv` package is installed. You can install it using `pip`:

```sh
pip install python-dotenv
```

#### Create a `.env` File

Create a file named `.env` in the root directory of your project. This file will store your environment variables.

#### Add Environment Variables

Add the following environment variables to the `.env` file:

```
FLASK_DB_HOST=localhost
FLASK_DB_USER=root
FLASK_DB_PASSWORD=your_password_here
FLASK_DB_NAME=stock_portfolio
```

Replace `your_password_here` with your actual MySQL root password.

#### Load Environment Variables

Ensure your Python scripts are set up to load these environment variables. The `initialize_db.py` and `app.py` files should include the following lines to load the environment variables from the `.env` file:

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```sh
pip install -r requirements.txt
```

### 4. Run the Flask Application

Start the Flask application:

```sh
python app.py
```

The application will be accessible at `http://127.0.0.1:5000`.

## Project Structure

```
investwise-project/
├── app.py
├── data_service/
│   ├── __init__.py
│   ├── initialize_db.py
├── static/
│   ├── style.css
├── templates/
│   ├── index.html
├── .env
├── requirements.txt
└── README.md
```

## Usage

- Enter a stock ticker symbol (e.g., AAPL for Apple, GOOGL for Google) in the input box and click "View Chart" to see the stock's performance.
- Select a time range (1 Year, 6 Months, 3 Months, 1 Month) to adjust the chart.
- Click the "Buy/Sell" button to open the transaction modal, where you can buy or sell shares of the selected stock.
- The additional information section provides details such as the stock's opening price, high, low, volume, market cap, and more.
- Use the simulator to practice your investing skills and track how your decisions impact your portfolio.

## Disclaimer

This is a training project for educational purposes and is not a real trading platform. The information provided here should not be considered financial advice. Always do your own research before making any investment decisions.
