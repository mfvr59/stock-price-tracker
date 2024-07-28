from flask import Flask, request, render_template, send_from_directory
import yfinance as yf
import matplotlib.pyplot as plt
import os
import numpy as np
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    app.logger.debug("Home page accessed")
    return render_template('index.html')

@app.route('/get_stock', methods=['POST'])
def get_stock():
    ticker = request.form['ticker'].upper()
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    app.logger.debug(f"Form data - Ticker: {ticker}, Start date: {start_date}, End date: {end_date}")
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        if hist.empty:
            app.logger.error(f"No data found for ticker: {ticker}")
            return "No data found for the given ticker and date range."

        # Save plot to a file
        plot_filename = f'static/{ticker}.png'
        plt.figure(figsize=(10, 6))
        plt.plot(hist.index, hist['Close'], label=ticker)
        plt.title(f"{ticker} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.savefig(plot_filename)
        plt.close()

        initial_price = np.array(hist['Close'])[0]
        final_price = np.array(hist['Close'])[-1]
        percentage_change = ((final_price - initial_price) / initial_price) * 100
        
        app.logger.debug(f"Stock data - Initial price: {initial_price}, Final price: {final_price}, Percentage change: {percentage_change}")
        
        return render_template('result.html', plot_url=plot_filename, ticker=ticker, percentage_change=percentage_change)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
