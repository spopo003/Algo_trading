from flask import Blueprint, render_template, jsonify
from .data_fetch import get_stock_data, simple_factor_investing, calculate_portfolio_metrics
import plotly.express as px
import plotly.utils
import json

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', message='Welcome to ALgo Trading Dashboard')

@main.route('/historical-prices')
def historical_prices():
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2023-01-01'
    end_date = '2024-01-01'

    prices = get_stock_data(tickers, start_date, end_date).reset_index()

    # Create a Plotly line chart for historical prices
    fig = px.line(prices, x='Date', y=prices.columns[1:], title='Historical Stock Prices')

    # Convert the Plotly figure to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Return the JSON response directly
    return jsonify(graph_json=graph_json)


@main.route('/portfolio')
def portfolio():
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    
    prices = get_stock_data(tickers, start_date, end_date)
    weights = simple_factor_investing(prices).to_dict()
    
    return jsonify(weights)

@main.route('/portfolio-weights')
def portfolio_weights():
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2023-01-01'
    end_date = '2024-01-01'

    prices = get_stock_data(tickers, start_date, end_date)
    weights = simple_factor_investing(prices)

    # Reset index so stock symbols are in a column
    weights = weights.reset_index()
    weights.columns = ['Stock', 'Weight']  # Rename columns for clarity

    print(weights)  # Debugging: Ensure the DataFrame is correctly formatted

    # Create a Plotly pie chart
    fig = px.pie(weights, names='Stock', values='Weight', title='Portfolio Weights')

    # Convert the Plotly figure to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Return the JSON response
    return jsonify(graph_json=graph_json)

@main.route('/portoflio-metrics')
def portfolio_metrics():
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    
    prices = get_stock_data(tickers, start_date, end_date)
    weights = simple_factor_investing(prices).reset_index()

    weights.columns = ['Stock', 'Weight']
    
    metrics = calculate_portfolio_metrics(weights, prices)
    
    return jsonify(metrics)
    
