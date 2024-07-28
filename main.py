import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def get_stock_prices(tickers):
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[0]
        print(f"The current price of {ticker} is ${price:.2f}")

def get_historical_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    return hist

def plot_stock_data(ticker, hist):
    if hist is not None:
        plt.figure(figsize=(10, 6))
        plt.plot(hist.index, hist['Close'], label=ticker)
        plt.title(f"{ticker} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.show()

def calculate_percentage_change(hist):
    if hist is not None:
        initial_price = hist['Close'].iloc[0]
        final_price = hist['Close'].iloc[-1]
        percentage_change = ((final_price - initial_price) / initial_price) * 100
        return percentage_change
    return None

if __name__ == "__main__":
    tickers = input("Enter stock ticker symbols separated by commas: ").split(',')
    tickers = [ticker.strip().upper() for ticker in tickers]
    
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    for ticker in tickers:
        get_stock_prices([ticker])
        
        hist_data = get_historical_data(ticker, start_date, end_date)
        if hist_data is not None:
            plot_stock_data(ticker, hist_data)
            
            percentage_change = calculate_percentage_change(hist_data)
            if percentage_change is not None:
                print(f"The percentage change in price for {ticker} from {start_date} to {end_date} is {percentage_change:.2f}%")

