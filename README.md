# Flask Stock Portfolio

A simple web application to display a user's stock portfolio using Flask as the backend and Bootstrap for the frontend.

## Project Structure

```
flask_portfolio/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── venv/
```

## Requirements

- Python 3.x
- Flask

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/flask_portfolio.git
   cd flask_portfolio
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Flask**:
   ```bash
   pip install Flask
   ```

## Running the Application

1. **Run the Flask app**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   Open a web browser and go to `http://127.0.0.1:5000/`.

## Application Details

The application displays a user's stock portfolio with hardcoded data for simplicity. You can extend this by fetching data from a database or an external API.