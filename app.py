"""
Business Analytics Dashboard - Web Application
Flask-based web application for interactive business analytics
"""

from flask import Flask, render_template, jsonify, request, send_file
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'business-analytics-dashboard-2025'

# Set style for better looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load and prepare the data
def load_data(filepath='DevicesData.xlsx'):
    """Load and clean the stock data"""
    try:
        df = pd.read_excel(filepath)
        # Split the single column into multiple columns
        df_split = df.iloc[:, 0].str.split(',', expand=True)
        df_split.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

        # Convert data types
        df_split['Date'] = pd.to_datetime(df_split['Date'])
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
            df_split[col] = pd.to_numeric(df_split[col], errors='coerce')

        # Set Date as index
        df_split.set_index('Date', inplace=True)
        return df_split
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Analytics functions
def descriptive_analytics(df):
    """Basic descriptive statistics and data overview"""
    if df is None:
        return {}
    
    return {
        'data_period': f"{df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}",
        'total_trading_days': f"{len(df):,}",
        'average_daily_volume': f"{df['Volume'].mean():,.0f}",
        'price_range': f"${df['Low'].min():.2f} - ${df['High'].max():.2f}",
        'average_closing_price': f"${df['Close'].mean():.2f}",
        'current_price': f"${df['Close'].iloc[-1]:.2f}"
    }

def performance_analytics(df):
    """Returns and performance metrics"""
    if df is None:
        return {}
    
    df['Daily_Return'] = df['Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod()
    
    total_return = df['Cumulative_Return'].iloc[-1] - 1
    annual_return = (df['Cumulative_Return'].iloc[-1] ** (252/len(df))) - 1
    volatility = df['Daily_Return'].std() * np.sqrt(252)
    
    return {
        'total_return': f"{total_return:.2%}",
        'annualized_return': f"{annual_return:.2%}",
        'annualized_volatility': f"{volatility:.2%}",
        'current_volatility': f"{df['Daily_Return'].std() * np.sqrt(252):.2%}"
    }

def technical_analytics(df):
    """Technical indicators"""
    if df is None:
        return {}
    
    # Simple Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # RSI
    def calculate_rsi(data, window=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    df['RSI'] = calculate_rsi(df['Close'])
    
    current_price = df['Close'].iloc[-1]
    current_sma_20 = df['SMA_20'].iloc[-1]
    current_sma_50 = df['SMA_50'].iloc[-1]
    current_rsi = df['RSI'].iloc[-1]
    
    signal = "BULLISH" if current_price > current_sma_50 else "BEARISH"
    
    return {
        'current_price': f"${current_price:.2f}",
        'sma_20': f"${current_sma_20:.2f}",
        'sma_50': f"${current_sma_50:.2f}",
        'rsi': f"{current_rsi:.1f}",
        'signal': signal,
        'signal_color': 'green' if signal == 'BULLISH' else 'red'
    }

def risk_analytics(df):
    """Risk metrics and VaR"""
    if df is None:
        return {}
    
    returns = df['Close'].pct_change().dropna()
    
    # Value at Risk (95% confidence)
    var_95 = np.percentile(returns, 5)
    
    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Sharpe Ratio (assuming 2% risk-free rate)
    risk_free_rate = 0.02
    excess_returns = returns - risk_free_rate/252
    sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns.std()
    
    return {
        'var_95': f"{var_95:.2%}",
        'max_drawdown': f"{max_drawdown:.2%}",
        'sharpe_ratio': f"{sharpe_ratio:.2f}",
        'risk_level': 'High' if abs(max_drawdown) > 0.5 else 'Medium' if abs(max_drawdown) > 0.2 else 'Low'
    }

# Chart generation functions
def create_price_chart(df):
    """Create price history chart"""
    if df is None:
        return None
    
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price', linewidth=2, color='blue')
    plt.plot(df.index, df['Close'].rolling(window=50).mean(), label='50-day SMA', linewidth=2, color='red')
    plt.title('Stock Price History with 50-day SMA', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Convert to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

def create_volume_chart(df):
    """Create volume chart"""
    if df is None:
        return None
    
    plt.figure(figsize=(12, 4))
    plt.bar(df.index, df['Volume'], color='orange', alpha=0.7)
    plt.title('Trading Volume History', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Volume', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Convert to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

def create_returns_chart(df):
    """Create returns distribution chart"""
    if df is None:
        return None
    
    df['Daily_Return'] = df['Close'].pct_change()
    returns = df['Daily_Return'].dropna()
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(returns, bins=50, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Daily Returns Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Daily Returns', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    df['Cumulative_Return'] = (1 + returns).cumprod()
    plt.plot(df.index, df['Cumulative_Return'], color='green', linewidth=2)
    plt.title('Cumulative Returns', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.tight_layout()
    
    # Convert to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

def create_risk_chart(df):
    """Create risk analysis chart"""
    if df is None:
        return None
    
    df['Daily_Return'] = df['Close'].pct_change()
    returns = df['Daily_Return'].dropna()
    
    # Calculate drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    
    plt.figure(figsize=(12, 6))
    plt.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red', label='Drawdown')
    plt.plot(drawdown.index, drawdown, color='darkred', linewidth=2)
    plt.title('Maximum Drawdown Analysis', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Drawdown', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    plt.tight_layout()
    
    # Convert to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    # Load data
    df = load_data()
    
    if df is None:
        return render_template('error.html', message="Data file not found or corrupted")
    
    # Run analytics
    descriptive = descriptive_analytics(df)
    performance = performance_analytics(df)
    technical = technical_analytics(df)
    risk = risk_analytics(df)
    
    # Generate charts
    price_chart = create_price_chart(df)
    volume_chart = create_volume_chart(df)
    returns_chart = create_returns_chart(df)
    risk_chart = create_risk_chart(df)
    
    return render_template('dashboard.html', 
                         descriptive=descriptive,
                         performance=performance,
                         technical=technical,
                         risk=risk,
                         price_chart=price_chart,
                         volume_chart=volume_chart,
                         returns_chart=returns_chart,
                         risk_chart=risk_chart)

@app.route('/api/analytics')
def api_analytics():
    """API endpoint for analytics data"""
    df = load_data()
    
    if df is None:
        return jsonify({'error': 'Data not found'}), 404
    
    # Return all analytics as JSON
    return jsonify({
        'descriptive': descriptive_analytics(df),
        'performance': performance_analytics(df),
        'technical': technical_analytics(df),
        'risk': risk_analytics(df)
    })

@app.route('/api/chart/<chart_type>')
def api_chart(chart_type):
    """API endpoint for charts"""
    df = load_data()
    
    if df is None:
        return jsonify({'error': 'Data not found'}), 404
    
    # Generate requested chart
    if chart_type == 'price':
        chart_url = create_price_chart(df)
    elif chart_type == 'volume':
        chart_url = create_volume_chart(df)
    elif chart_type == 'returns':
        chart_url = create_returns_chart(df)
    elif chart_type == 'risk':
        chart_url = create_risk_chart(df)
    else:
        return jsonify({'error': 'Invalid chart type'}), 400
    
    return jsonify({'chart_url': chart_url})

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')

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
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Local development setup
    if not os.path.exists('static'):
        os.makedirs('static')
        os.makedirs('static/css')
        os.makedirs('static/js')
    
    print("🚀 Starting Business Analytics Dashboard Web Application")
    print("📊 Open your browser and go to: http://localhost:5000")
    print("📈 Dashboard available at: http://localhost:5000/dashboard")
    print("📚 Documentation at: http://localhost:5000/documentation")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
