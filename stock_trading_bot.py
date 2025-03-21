import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from alpha_vantage.timeseries import TimeSeries

# --- Step 1: Fetch Stock Market Data from Alpha Vantage ---
def fetch_stock_data(ticker, start_date, end_date, api_key, retries=3, delay=5):
    ts = TimeSeries(key=api_key, output_format='pandas')
    for attempt in range(retries):
        try:
            data, _ = ts.get_daily(symbol=ticker, outputsize='full')
            data.index = pd.to_datetime(data.index)
            data = data['4. close'].rename('Close').to_frame()
            filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
            if filtered_data.empty:
                raise ValueError(f"No data returned for {ticker} between {start_date} and {end_date}.")
            return filtered_data.sort_index()
        except Exception as e:
            print(f"Error fetching data: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    print(f"Failed to fetch data for {ticker} after {retries} attempts. Using sample data.")
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    return pd.DataFrame({'Close': np.random.uniform(100, 150, len(dates))}, index=dates)

# Configuration
ticker = "AAPL"
start_date = "2023-10-01"
end_date = "2025-03-21"
api_key = "YOUR_API_KEY"  # Replace with your Alpha Vantage API key

# Fetch real data
stock_data = fetch_stock_data(ticker, start_date, end_date, api_key)
print(f"Fetched {len(stock_data)} days of data.")

# --- Step 2: Define Advanced Trading Strategy ---
stock_data['SMA10'] = stock_data['Close'].rolling(window=10).mean()
stock_data['SMA30'] = stock_data['Close'].rolling(window=30).mean()
stock_data['EMA10'] = stock_data['Close'].ewm(span=10, adjust=False).mean()
stock_data['EMA30'] = stock_data['Close'].ewm(span=30, adjust=False).mean()
stock_data['ATR'] = stock_data['Close'].rolling(14).std()  # Approximate ATR

# Generate trading signals
stock_data['Signal'] = 0
mask = (stock_data['SMA10'] > stock_data['SMA30']) & (stock_data.index >= stock_data.index[29])
stock_data.loc[mask, 'Signal'] = 1
stock_data['Position'] = stock_data['Signal'].diff()

# --- Step 3: Simulate Trading with Stop-Loss & Take-Profit ---
initial_cash = 10000
cash = initial_cash
shares = 0
portfolio_value = []
buy_price = 0
stop_loss = 0
take_profit = 0

for index, row in stock_data.iterrows():
    if row['Position'] == 1:  # Buy signal
        shares = cash // row['Close']
        cash -= shares * row['Close']
        buy_price = row['Close']
        stop_loss = buy_price * 0.95  # 5% below buy price
        take_profit = buy_price * 1.10  # 10% above buy price
        print(f"Buy {shares} shares at ${row['Close']:.2f} on {index.date()}")
    elif row['Position'] == -1 and shares > 0:  # Sell signal
        cash += shares * row['Close']
        print(f"Sell {shares} shares at ${row['Close']:.2f} on {index.date()}")
        shares = 0
    elif shares > 0 and (row['Close'] <= stop_loss or row['Close'] >= take_profit):
        cash += shares * row['Close']
        print(f"Stop-loss or Take-profit triggered: Sold {shares} shares at ${row['Close']:.2f} on {index.date()}")
        shares = 0
    
    total_value = cash + shares * row['Close']
    portfolio_value.append(total_value)

stock_data['Portfolio_Value'] = portfolio_value

# --- Step 4: Display Results ---
print("\n--- Trading Summary ---")
print(f"Initial Cash: ${initial_cash:.2f}")
print(f"Final Portfolio Value: ${stock_data['Portfolio_Value'].iloc[-1]:.2f}")
print(f"Profit/Loss: ${stock_data['Portfolio_Value'].iloc[-1] - initial_cash:.2f}")

# --- Step 5: Visualize Results ---
plt.figure(figsize=(14, 7))
plt.plot(stock_data['Close'], label='Close Price', alpha=0.5)
plt.plot(stock_data['SMA10'], label='10-Day SMA', alpha=0.75)
plt.plot(stock_data['SMA30'], label='30-Day SMA', alpha=0.75)
plt.plot(stock_data['EMA10'], label='10-Day EMA', linestyle='dotted')
plt.plot(stock_data['EMA30'], label='30-Day EMA', linestyle='dotted')

# Add buy/sell markers
buy_signals = stock_data[stock_data['Position'] == 1]['Close']
sell_signals = stock_data[stock_data['Position'] == -1]['Close']
plt.scatter(buy_signals.index, buy_signals, color='green', label='Buy', marker='^', s=100)
plt.scatter(sell_signals.index, sell_signals, color='red', label='Sell', marker='v', s=100)
plt.title(f'{ticker} Stock Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(14, 7))
plt.plot(stock_data['Portfolio_Value'], label='Portfolio Value', color='green')
plt.title('Portfolio Value Over Time')
plt.xlabel('Date')
plt.ylabel('Value (USD)')
plt.legend()
plt.grid(True)
plt.show()

print("\n--- Last 5 Rows of Data ---")
print(stock_data[['Close', 'SMA10', 'SMA30', 'EMA10', 'EMA30', 'Signal', 'Position', 'Portfolio_Value']].tail())