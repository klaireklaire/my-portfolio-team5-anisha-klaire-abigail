# Data Service Setup

This document provides instructions on how to set up environment variables for the Data Service using a `.env` file.

## Prerequisites

- Python 3.x
- `pip` package manager
- MySQL Server activated and connected
- `python-dotenv` package

## Setting Up Environment Variables

To keep sensitive information such as database credentials secure and configurable, we use environment variables stored in a `.env` file. Follow the steps below to set this up:

### 1. Install `python-dotenv`

Make sure the `python-dotenv` package is installed. You can install it using `pip`:

```sh
pip install python-dotenv
```

### 2. Create a `.env` File

Create a file named `.env` in the root directory of your project. This file will store your environment variables.

### 3. Add Environment Variables

Add the following environment variables to the `.env` file:

```
FLASK_DB_HOST=localhost
FLASK_DB_USER=root
FLASK_DB_PASSWORD=your_password_here
FLASK_DB_NAME=stock_portfolio
```

Replace `your_password_here` with your actual MySQL root password.

### 4. Load Environment Variables

Ensure your Python scripts are set up to load these environment variables. The `initialize_db.py` and `app.py` files should include the following lines to load the environment variables from the `.env` file:

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
```
