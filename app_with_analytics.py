"""
Simple Business Analytics Dashboard - Vercel Compatible
Minimal Flask app that works reliably in serverless environment
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'business-analytics-dashboard-2025'

# Sample data generator
def create_sample_data():
    """Create sample data for demonstration"""
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    np.random.seed(42)
    
    # Generate realistic stock-like data
    price = 100 + np.cumsum(np.random.randn(len(dates)) * 0.02)
    volume = np.random.randint(1000000, 5000000, len(dates))
    
    data = {
        'Open': price * (1 + np.random.randn(len(dates)) * 0.01),
        'High': price * (1 + np.abs(np.random.randn(len(dates))) * 0.02),
        'Low': price * (1 - np.abs(np.random.randn(len(dates))) * 0.02),
        'Close': price,
        'Adj Close': price,
        'Volume': volume
    }
    
    df = pd.DataFrame(data, index=dates)
    return df

# Load data (always use sample data for reliability)
df = create_sample_data()

# Basic analytics
def get_basic_analytics():
    """Get basic analytics without charts"""
    if df is None or len(df) == 0:
        return {}
    
    return {
        'data_period': f"{df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}",
        'total_trading_days': f"{len(df):,}",
        'average_volume': f"{df['Volume'].mean():,.0f}",
        'price_range': f"${df['Close'].min():.2f} - ${df['Close'].max():.2f}",
        'total_return': f"{((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100:.1f}%",
        'current_price': f"${df['Close'].iloc[-1]:.2f}",
        'volatility': f"{df['Close'].pct_change().std() * np.sqrt(252) * 100:.1f}%"
    }

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    analytics = get_basic_analytics()
    return render_template('dashboard.html', analytics=analytics)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')

@app.route('/api/analytics')
def api_analytics():
    """API endpoint for analytics data"""
    return jsonify(get_basic_analytics())

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Vercel serverless handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    print("🚀 Starting Simple Business Analytics Dashboard")
    print("📊 Open your browser and go to: http://localhost:5000")
    print("📈 Dashboard available at: http://localhost:5000/dashboard")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
