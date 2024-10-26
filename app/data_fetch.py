import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(tickers, start_date, end_date):
    """
    Fetches historical stock prices for given tickers
    
    Args:s
        tickers (list): List of stock symbols (e.g., ['AAPL', 'GOOGL']).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        
    Returns:
        DataFrame: A DataFrame containing stock prices
    """
    
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']


def simple_factor_investing(prices):
    """
    Allocates portfolio weights based on returns.

    Args:
        prices (DataFrame): Historical stock prices.
        
    Returns:
        DataFrame: DataFrame containing stock weights
    """
    
    # Calculate average daily rerutns for each stock
    returns = prices.pct_change().mean()
    
    # Normalize weights (inverse returns to short overvalued stocks)
    weights = returns / returns.abs().sum()
    
    # Convert to DataFrame for display
    weights_df = pd.DataFrame(weights, columns=['Weight'])
    return weights_df
    
def calculate_portfolio_metrics(weights, prices, risk_free_rate=0.02):
    """
    Calculate expected return, volatility, and Sharpe ratio of the portfolio.

    Args:
        weights (DataFrame): Portfolio weights (one row per stock)
        prices (DataFrame): Historical stock prices
        risk_free_rate (float, optional): Annual risk-free rate. Defaults to 0.02.
        
    Returns
        dict: Portfolio metrics (expected returns, volatility, Sharpe Ratio).
    """
    daily_returns = prices.pct_change().dropna()
    
    portfolio_return = np.dot(daily_returns.mean(), weights['Weight'])
    
    portfolio_volatility = np.sqrt(np.dot(weights['Weight'].T, np.dot(daily_returns.cov(), weights['Weight'])))
    
    sharpe_ratio = (portfolio_return * 252 -risk_free_rate)/(portfolio_volatility * np.sqrt(252))
    
    return {
        'Expected Return': round(portfolio_return * 252),
        'Volatility': round(portfolio_volatility * np.sqrt(252), 4),
        'Sharpe Ratio': round(sharpe_ratio, 4)
    }
# example use
if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    
    prices = get_stock_data(tickers, start_date, end_date)
    print(prices.head())
    