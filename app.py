from flask import Flask, request, render_template
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_stock', methods=['POST'])
def get_stock():
    ticker = request.form['ticker'].upper()
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        if hist.empty:
            return "No data found for the given ticker and date range."

        img = io.BytesIO()
        plt.figure(figsize=(10, 6))
        plt.plot(hist.index, hist['Close'], label=ticker)
        plt.title(f"{ticker} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        
        initial_price = hist['Close'].iloc[0]
        final_price = hist['Close'].iloc[-1]
        percentage_change = ((final_price - initial_price) / initial_price) * 100
        
        return render_template('result.html', plot_url=plot_url, ticker=ticker, percentage_change=percentage_change)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)