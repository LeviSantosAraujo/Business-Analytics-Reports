import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Create reports directory
if not os.path.exists('reports'):
    os.makedirs('reports')
    os.makedirs('reports/charts')

# Load and prepare the data
def load_data(filepath):
    """Load and clean the stock data"""
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

# 1. DESCRIPTIVE ANALYTICS
def descriptive_analytics(df):
    """Basic descriptive statistics and data overview"""
    report = []
    report.append("=== DESCRIPTIVE ANALYTICS REPORT ===")
    report.append(f"Data period: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    report.append(f"Total trading days: {len(df):,}")
    report.append(f"Average daily volume: {df['Volume'].mean():,.0f}")
    report.append(f"Price range: ${df['Low'].min():.2f} - ${df['High'].max():.2f}")
    report.append(f"Average closing price: ${df['Close'].mean():.2f}")
    report.append("\nPrice Statistics:")
    report.append(df[['Open', 'High', 'Low', 'Close']].describe().to_string())
    report.append("\nVolume Statistics:")
    report.append(df['Volume'].describe().to_string())
    
    # Create chart
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['Close'], label='Close Price', color='blue', linewidth=1)
    plt.title('Stock Price History - Descriptive Analytics')
    plt.ylabel('Price ($)')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.bar(df.index, df['Volume'], color='orange', alpha=0.7)
    plt.title('Trading Volume History')
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('reports/charts/01_descriptive_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/01_descriptive_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

# 2. PERFORMANCE ANALYTICS
def performance_analytics(df):
    """Returns and performance metrics"""
    df['Daily_Return'] = df['Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod()
    
    total_return = df['Cumulative_Return'].iloc[-1] - 1
    annual_return = (df['Cumulative_Return'].iloc[-1] ** (252/len(df))) - 1
    volatility = df['Daily_Return'].std() * np.sqrt(252)
    
    report = []
    report.append("=== PERFORMANCE ANALYTICS REPORT ===")
    report.append(f"Total return: {total_return:.2%}")
    report.append(f"Annualized return: {annual_return:.2%}")
    report.append(f"Annualized volatility: {volatility:.2%}")
    
    # Create chart
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Cumulative_Return'], label='Cumulative Return', color='green', linewidth=2)
    plt.title('Cumulative Returns - Performance Analytics')
    plt.ylabel('Cumulative Return')
    plt.xlabel('Date')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format y-axis as percentage
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.tight_layout()
    plt.savefig('reports/charts/02_performance_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/02_performance_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

# 3. TECHNICAL ANALYSIS
def technical_analysis(df):
    """Technical indicators"""
    # Simple Moving Average
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
    current_sma = df['SMA_50'].iloc[-1]
    current_rsi = df['RSI'].iloc[-1]
    
    report = []
    report.append("=== TECHNICAL ANALYTICS REPORT ===")
    report.append(f"Current price: ${current_price:.2f}")
    report.append(f"50-day SMA: ${current_sma:.2f}")
    report.append(f"RSI (14-day): {current_rsi:.1f}")
    
    if current_price > current_sma:
        report.append("Signal: BULLISH (price above SMA)")
    else:
        report.append("Signal: BEARISH (price below SMA)")
    
    # Create chart
    plt.figure(figsize=(12, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(df.index, df['Close'], label='Close Price', color='blue', linewidth=1)
    plt.plot(df.index, df['SMA_50'], label='50-day SMA', color='red', linewidth=2)
    plt.title('Price and Moving Average - Technical Analysis')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(3, 1, 2)
    plt.plot(df.index, df['RSI'], label='RSI', color='purple', linewidth=1)
    plt.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
    plt.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
    plt.title('RSI Indicator')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(3, 1, 3)
    plt.bar(df.index[-252:], df['Volume'][-252:], color='orange', alpha=0.7)
    plt.title('Recent Trading Volume (Last 252 days)')
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('reports/charts/03_technical_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/03_technical_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

# 4. RISK ANALYTICS
def risk_analytics(df):
    """Risk metrics and VaR"""
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
    
    report = []
    report.append("=== RISK ANALYTICS REPORT ===")
    report.append(f"Value at Risk (95% confidence, daily): {var_95:.2%}")
    report.append(f"Maximum drawdown: {max_drawdown:.2%}")
    report.append(f"Sharpe ratio: {sharpe_ratio:.2f}")
    
    # Create chart
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.hist(returns, bins=50, alpha=0.7, color='red', edgecolor='black')
    plt.axvline(var_95, color='darkred', linestyle='--', linewidth=2, label=f'VaR 95%: {var_95:.2%}')
    plt.title('Distribution of Daily Returns - Risk Analytics')
    plt.xlabel('Daily Returns')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(drawdown.index, drawdown, color='darkred', linewidth=1)
    plt.title('Drawdown Analysis')
    plt.ylabel('Drawdown')
    plt.xlabel('Date')
    plt.grid(True, alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.tight_layout()
    plt.savefig('reports/charts/04_risk_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/04_risk_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

# 5. TIME SERIES ANALYSIS
def time_series_analysis(df):
    """Trend and seasonality analysis"""
    # Monthly returns pattern
    monthly_returns = df['Close'].resample('M').last().pct_change()
    avg_monthly_return = monthly_returns.groupby(monthly_returns.index.month).mean()
    
    best_month = avg_monthly_return.idxmax()
    worst_month = avg_monthly_return.idxmin()
    
    report = []
    report.append("=== TIME SERIES ANALYTICS REPORT ===")
    report.append(f"Best performing month: {best_month} ({avg_monthly_return.max():.2%})")
    report.append(f"Worst performing month: {worst_month} ({avg_monthly_return.min():.2%})")
    
    # Long-term trend
    yearly_avg = df['Close'].resample('Y').mean()
    recent_trend = yearly_avg.tail(5).pct_change().mean()
    
    report.append(f"Recent 5-year trend: {recent_trend:.2%} per year")
    
    # Create chart
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_returns = [avg_monthly_return.get(i, 0) for i in range(1, 13)]
    colors = ['green' if x > 0 else 'red' for x in month_returns]
    
    plt.bar(months, month_returns, color=colors, alpha=0.7)
    plt.title('Average Monthly Returns - Time Series Analysis')
    plt.ylabel('Average Return')
    plt.xlabel('Month')
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.subplot(2, 1, 2)
    plt.plot(yearly_avg.index, yearly_avg, marker='o', linewidth=2, markersize=4)
    plt.title('Yearly Average Price Trend')
    plt.ylabel('Average Price ($)')
    plt.xlabel('Year')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('reports/charts/05_time_series_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/05_time_series_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

# 6. VOLATILITY ANALYSIS
def volatility_analysis(df):
    """Volatility patterns and clustering"""
    df['Daily_Return'] = df['Close'].pct_change()
    df['Volatility_30d'] = df['Daily_Return'].rolling(window=30).std() * np.sqrt(252)
    
    current_vol = df['Volatility_30d'].iloc[-1]
    avg_vol = df['Volatility_30d'].mean()
    high_vol_threshold = df['Volatility_30d'].quantile(0.8)
    
    report = []
    report.append("=== VOLATILITY ANALYTICS REPORT ===")
    report.append(f"Current 30-day volatility: {current_vol:.2%}")
    report.append(f"Average volatility: {avg_vol:.2%}")
    report.append(f"High volatility threshold (80th percentile): {high_vol_threshold:.2%}")
    
    if current_vol > high_vol_threshold:
        report.append("Current market condition: HIGH VOLATILITY")
    else:
        report.append("Current market condition: NORMAL VOLATILITY")
    
    # Create chart
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Volatility_30d'], label='30-day Volatility', color='orange', linewidth=1.5)
    plt.axhline(y=avg_vol, color='blue', linestyle='--', label=f'Average: {avg_vol:.2%}')
    plt.axhline(y=high_vol_threshold, color='red', linestyle='--', label=f'High Vol Threshold: {high_vol_threshold:.2%}')
    plt.title('Volatility Analysis - Rolling 30-day Volatility')
    plt.ylabel('Annualized Volatility')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.tight_layout()
    plt.savefig('reports/charts/06_volatility_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/06_volatility_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

# 7. PREDICTIVE ANALYTICS
def predictive_analytics(df):
    """Simple prediction using moving averages"""
    # Simple momentum strategy
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # Generate signals
    current_price = df['Close'].iloc[-1]
    sma_20 = df['SMA_20'].iloc[-1]
    sma_50 = df['SMA_50'].iloc[-1]
    
    # Golden Cross/Death Cross
    if sma_20 > sma_50 and df['SMA_20'].iloc[-2] <= df['SMA_50'].iloc[-2]:
        prediction = "GOLDEN CROSS - Bullish signal"
    elif sma_20 < sma_50 and df['SMA_20'].iloc[-2] >= df['SMA_50'].iloc[-2]:
        prediction = "DEATH CROSS - Bearish signal"
    elif sma_20 > sma_50:
        prediction = "Bullish trend continuation"
    else:
        prediction = "Bearish trend continuation"
    
    report = []
    report.append("=== PREDICTIVE ANALYTICS REPORT ===")
    report.append(f"20-day SMA: ${sma_20:.2f}")
    report.append(f"50-day SMA: ${sma_50:.2f}")
    report.append(f"Prediction: {prediction}")
    
    # Create chart
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(df.index[-252:], df['Close'][-252:], label='Close Price', color='blue', linewidth=1)
    plt.plot(df.index[-252:], df['SMA_20'][-252:], label='20-day SMA', color='green', linewidth=2)
    plt.plot(df.index[-252:], df['SMA_50'][-252:], label='50-day SMA', color='red', linewidth=2)
    plt.title('Moving Average Crossover - Predictive Analytics')
    plt.ylabel('Price ($)')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Signal visualization
    plt.subplot(2, 1, 2)
    signals = np.where(df['SMA_20'] > df['SMA_50'], 1, -1)
    plt.plot(df.index[-252:], signals[-252:], marker='o', linewidth=2, markersize=3)
    plt.title('Trading Signals (1=Bullish, -1=Bearish)')
    plt.ylabel('Signal')
    plt.xlabel('Date')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('reports/charts/07_predictive_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/07_predictive_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

# 8. TRADING STRATEGY ANALYSIS
def trading_strategy_analysis(df):
    """Backtest a simple trading strategy"""
    df['Daily_Return'] = df['Close'].pct_change()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    
    # Strategy: Buy when price > SMA_20, Sell when price < SMA_20
    df['Signal'] = np.where(df['Close'] > df['SMA_20'], 1, -1)
    df['Strategy_Return'] = df['Signal'].shift(1) * df['Daily_Return']
    
    # Calculate performance
    strategy_cumulative = (1 + df['Strategy_Return'].dropna()).cumprod()
    buy_hold_cumulative = (1 + df['Daily_Return'].dropna()).cumprod()
    
    strategy_return = strategy_cumulative.iloc[-1] - 1
    buy_hold_return = buy_hold_cumulative.iloc[-1] - 1
    
    report = []
    report.append("=== TRADING STRATEGY ANALYTICS REPORT ===")
    report.append(f"Strategy total return: {strategy_return:.2%}")
    report.append(f"Buy & Hold return: {buy_hold_return:.2%}")
    report.append(f"Strategy outperformance: {strategy_return - buy_hold_return:.2%}")
    
    if strategy_return > buy_hold_return:
        report.append("Result: Strategy BEATS Buy & Hold")
    else:
        report.append("Result: Buy & Hold BEATS Strategy")
    
    # Create chart
    plt.figure(figsize=(12, 6))
    plt.plot(strategy_cumulative.index, strategy_cumulative, label='SMA Strategy', color='blue', linewidth=2)
    plt.plot(buy_hold_cumulative.index, buy_hold_cumulative, label='Buy & Hold', color='green', linewidth=2)
    plt.title('Strategy Performance Comparison - Trading Strategy Analytics')
    plt.ylabel('Cumulative Return')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.tight_layout()
    plt.savefig('reports/charts/08_trading_strategy_analytics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save report
    with open('reports/08_trading_strategy_analytics.txt', 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report)

def main():
    """Generate all reports and charts"""
    print("GENERATING COMPREHENSIVE BUSINESS ANALYTICS REPORTS")
    print("=" * 60)
    print()
    
    # Load data
    df = load_data('DevicesData.xlsx')
    
    # Generate all reports
    reports = []
    reports.append(descriptive_analytics(df))
    reports.append(performance_analytics(df))
    reports.append(technical_analysis(df))
    reports.append(risk_analytics(df))
    reports.append(time_series_analysis(df))
    reports.append(volatility_analysis(df))
    reports.append(predictive_analytics(df))
    reports.append(trading_strategy_analysis(df))
    
    # Generate summary report
    summary_report = "BUSINESS ANALYTICS SUMMARY REPORT\n"
    summary_report += "=" * 50 + "\n\n"
    summary_report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary_report += f"Data analyzed: {len(df):,} trading days\n"
    summary_report += f"Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}\n\n"
    summary_report += "Reports Generated:\n"
    summary_report += "1. Descriptive Analytics - Basic statistics and overview\n"
    summary_report += "2. Performance Analytics - Returns and volatility metrics\n"
    summary_report += "3. Technical Analytics - Moving averages and RSI indicators\n"
    summary_report += "4. Risk Analytics - VaR and drawdown analysis\n"
    summary_report += "5. Time Series Analytics - Seasonality and trends\n"
    summary_report += "6. Volatility Analytics - Volatility patterns\n"
    summary_report += "7. Predictive Analytics - Moving average crossovers\n"
    summary_report += "8. Trading Strategy Analytics - Strategy backtesting\n\n"
    summary_report += "Files Generated:\n"
    summary_report += "- 8 text reports in 'reports/' folder\n"
    summary_report += "- 8 charts in 'reports/charts/' folder\n"
    
    with open('reports/SUMMARY_REPORT.txt', 'w') as f:
        f.write(summary_report)
    
    print("✓ All reports generated successfully!")
    print("✓ Charts saved in 'reports/charts/' folder")
    print("✓ Text reports saved in 'reports/' folder")
    print("✓ Summary report saved as 'reports/SUMMARY_REPORT.txt'")
    print()
    print("Generated Files:")
    for i in range(1, 9):
        print(f"  - reports/0{i}_analytics.txt")
        print(f"  - reports/charts/0{i}_analytics.png")
    print("  - reports/SUMMARY_REPORT.txt")

if __name__ == "__main__":
    main()
