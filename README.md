# Stock Trading Bot
- The Stock Trading Bot is designed to introduce you to financial datasets and AI-driven decision-making. It automates stock trading by fetching real-time market data, analyzing trends, and executing trades based on predefined strategies. This project is a great way to explore reinforcement learning, real-time data processing, and financial AI applications.

## Features
- Real-time Stock Market Data Fetching using Yahoo Finance or Alpaca API.
- Moving Average Crossover Strategy (SMA & EMA) for trade signals.
- Stop-Loss & Take-Profit Mechanisms for risk management.
- Volatility Analysis using Average True Range (ATR).
- Automated Trade Execution & Portfolio Tracking.
- Data Visualization for performance analysis.

## Tools & Technologies
- Data Fetching: yfinance (Yahoo Finance API), alpaca-trade-api (Alpaca API)
- Data Processing: pandas, numpy
- Visualization: matplotlib
- Backtesting & Strategy Implementation: Custom-built using Python

## Installation & Setup
1. Clone the repository:
- git clone https://github.com/yourusername/stock-trading-bot.git
- cd stock-trading-bot
2. Install dependencies
- pip install pandas numpy matplotlib yfinance alpaca-trade-api
3. Set up your API key:
- API_KEY = "your_alpaca_api_key"
4. Run the bot:
- python stock_trading_bot.py

## How It Works
- Fetch Stock Data: The bot retrieves historical and real-time stock prices.
- Analyze Trends: It calculates SMA (10-day & 30-day) and EMA (10-day & 30-day).
- Generate Trade Signals: Buy when short-term SMA/EMA crosses above long-term, and sell when it crosses below.
- Risk Management: Implements a stop-loss (5%) and take-profit (10%) strategy.
- Portfolio Management: Tracks cash, shares, and total portfolio value over time.
- Visualization: Plots stock price trends and portfolio performance.

## Impact
- This project automates trading strategies, helping users explore financial AI applications and understand real-time stock market behavior. It serves as a foundation for algorithmic trading, backtesting strategies, and reinforcement learning in finance.


## License
- This project is licensed under the MIT License.

## Author
- Developed by Melisa Sever.
- Feel free to contribute and explore the world of algorithmic trading! 🚀

