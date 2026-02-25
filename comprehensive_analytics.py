import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

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
    print("=== 1. DESCRIPTIVE ANALYTICS ===")
    print(f"Data period: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    print(f"Total trading days: {len(df):,}")
    print(f"Average daily volume: {df['Volume'].mean():,.0f}")
    print(f"Price range: ${df['Low'].min():.2f} - ${df['High'].max():.2f}")
    print(f"Average closing price: ${df['Close'].mean():.2f}")
    print()

# 2. PERFORMANCE ANALYTICS
def performance_analytics(df):
    """Returns and performance metrics"""
    print("=== 2. PERFORMANCE ANALYTICS ===")
    df['Daily_Return'] = df['Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod()
    
    total_return = df['Cumulative_Return'].iloc[-1] - 1
    annual_return = (df['Cumulative_Return'].iloc[-1] ** (252/len(df))) - 1
    volatility = df['Daily_Return'].std() * np.sqrt(252)
    
    print(f"Total return: {total_return:.2%}")
    print(f"Annualized return: {annual_return:.2%}")
    print(f"Annualized volatility: {volatility:.2%}")
    print()

# 3. TECHNICAL ANALYSIS
def technical_analysis(df):
    """Technical indicators"""
    print("=== 3. TECHNICAL ANALYTICS ===")
    
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
    
    print(f"Current price: ${current_price:.2f}")
    print(f"50-day SMA: ${current_sma:.2f}")
    print(f"RSI (14-day): {current_rsi:.1f}")
    
    if current_price > current_sma:
        print("Signal: BULLISH (price above SMA)")
    else:
        print("Signal: BEARISH (price below SMA)")
    print()

# 4. RISK ANALYTICS
def risk_analytics(df):
    """Risk metrics and VaR"""
    print("=== 4. RISK ANALYTICS ===")
    
    returns = df['Daily_Return'].dropna()
    
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
    
    print(f"Value at Risk (95% confidence, daily): {var_95:.2%}")
    print(f"Maximum drawdown: {max_drawdown:.2%}")
    print(f"Sharpe ratio: {sharpe_ratio:.2f}")
    print()

# 5. TIME SERIES ANALYSIS
def time_series_analysis(df):
    """Trend and seasonality analysis"""
    print("=== 5. TIME SERIES ANALYTICS ===")
    
    # Monthly returns pattern
    monthly_returns = df['Close'].resample('M').last().pct_change()
    avg_monthly_return = monthly_returns.groupby(monthly_returns.index.month).mean()
    
    best_month = avg_monthly_return.idxmax()
    worst_month = avg_monthly_return.idxmin()
    
    print(f"Best performing month: {best_month} ({avg_monthly_return.max():.2%})")
    print(f"Worst performing month: {worst_month} ({avg_monthly_return.min():.2%})")
    
    # Long-term trend
    yearly_avg = df['Close'].resample('Y').mean()
    recent_trend = yearly_avg.tail(5).pct_change().mean()
    
    print(f"Recent 5-year trend: {recent_trend:.2%} per year")
    print()

# 6. VOLATILITY ANALYSIS
def volatility_analysis(df):
    """Volatility patterns and clustering"""
    print("=== 6. VOLATILITY ANALYTICS ===")
    
    df['Daily_Return'] = df['Close'].pct_change()
    df['Volatility_30d'] = df['Daily_Return'].rolling(window=30).std() * np.sqrt(252)
    
    current_vol = df['Volatility_30d'].iloc[-1]
    avg_vol = df['Volatility_30d'].mean()
    high_vol_threshold = df['Volatility_30d'].quantile(0.8)
    
    print(f"Current 30-day volatility: {current_vol:.2%}")
    print(f"Average volatility: {avg_vol:.2%}")
    print(f"High volatility threshold (80th percentile): {high_vol_threshold:.2%}")
    
    if current_vol > high_vol_threshold:
        print("Current market condition: HIGH VOLATILITY")
    else:
        print("Current market condition: NORMAL VOLATILITY")
    print()

# 7. PREDICTIVE ANALYTICS
def predictive_analytics(df):
    """Simple prediction using moving averages"""
    print("=== 7. PREDICTIVE ANALYTICS ===")
    
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
    
    print(f"20-day SMA: ${sma_20:.2f}")
    print(f"50-day SMA: ${sma_50:.2f}")
    print(f"Prediction: {prediction}")
    print()

# 8. TRADING STRATEGY ANALYSIS
def trading_strategy_analysis(df):
    """Backtest a simple trading strategy"""
    print("=== 8. TRADING STRATEGY ANALYTICS ===")
    
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
    
    print(f"Strategy total return: {strategy_return:.2%}")
    print(f"Buy & Hold return: {buy_hold_return:.2%}")
    print(f"Strategy outperformance: {strategy_return - buy_hold_return:.2%}")
    
    if strategy_return > buy_hold_return:
        print("Result: Strategy BEATS Buy & Hold")
    else:
        print("Result: Buy & Hold BEATS Strategy")
    print()

# 9. MARKET SENTIMENT ANALYSIS
def market_sentiment_analysis(df):
    """Volume-price relationship analysis"""
    print("=== 9. MARKET SENTIMENT ANALYTICS ===")
    
    # Volume analysis
    avg_volume = df['Volume'].mean()
    current_volume = df['Volume'].iloc[-1]
    volume_ratio = current_volume / avg_volume
    
    # Price change on high volume days
    df['Daily_Return'] = df['Close'].pct_change()
    high_volume_days = df['Volume'] > df['Volume'].quantile(0.8)
    avg_return_high_vol = df['Daily_Return'][high_volume_days].mean()
    
    # Up/Down volume ratio
    up_days = df['Daily_Return'] > 0
    down_days = df['Daily_Return'] < 0
    up_volume = df['Volume'][up_days].sum()
    down_volume = df['Volume'][down_days].sum()
    volume_ratio_up_down = up_volume / down_volume if down_volume > 0 else float('inf')
    
    print(f"Current/Average volume ratio: {volume_ratio:.2f}")
    print(f"Average return on high-volume days: {avg_return_high_vol:.2%}")
    print(f"Up/Down volume ratio: {volume_ratio_up_down:.2f}")
    
    if volume_ratio_up_down > 1.2:
        print("Sentiment: BULLISH (more volume on up days)")
    elif volume_ratio_up_down < 0.8:
        print("Sentiment: BEARISH (more volume on down days)")
    else:
        print("Sentiment: NEUTRAL")
    print()

# 10. MARKET REGIME ANALYSIS
def market_regime_analysis(df):
    """Identify bull/bear market periods"""
    print("=== 10. MARKET REGIME ANALYTICS ===")
    
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Current regime
    current_price = df['Close'].iloc[-1]
    current_sma_200 = df['SMA_200'].iloc[-1]
    
    # Count days in each regime
    bull_days = (df['Close'] > df['SMA_200']).sum()
    bear_days = (df['Close'] <= df['SMA_200']).sum()
    total_days = len(df.dropna())
    
    bull_percentage = bull_days / total_days * 100
    bear_percentage = bear_days / total_days * 100
    
    print(f"Current price: ${current_price:.2f}")
    print(f"200-day SMA: ${current_sma_200:.2f}")
    
    if current_price > current_sma_200:
        print("Current regime: BULL MARKET")
    else:
        print("Current regime: BEAR MARKET")
    
    print(f"Historical bull market days: {bull_percentage:.1f}%")
    print(f"Historical bear market days: {bear_percentage:.1f}%")
    print()

# 11. CORRELATION ANALYSIS
def correlation_analysis(df):
    """Price-volume correlation analysis"""
    print("=== 11. CORRELATION ANALYTICS ===")
    
    df['Daily_Return'] = df['Close'].pct_change()
    df['Volume_Change'] = df['Volume'].pct_change()
    
    # Correlations
    price_volume_corr = df['Daily_Return'].corr(df['Volume_Change'])
    price_level_volume_corr = df['Close'].pct_change().corr(df['Volume'])
    
    # Autocorrelation
    return_autocorr = df['Daily_Return'].autocorr(lag=1)
    volume_autocorr = df['Volume'].pct_change().autocorr(lag=1)
    
    print(f"Daily return vs volume change correlation: {price_volume_corr:.3f}")
    print(f"Price level vs volume correlation: {price_level_volume_corr:.3f}")
    print(f"Return autocorrelation (1-day lag): {return_autocorr:.3f}")
    print(f"Volume change autocorrelation (1-day lag): {volume_autocorr:.3f}")
    
    if abs(price_volume_corr) > 0.3:
        print("Strong price-volume relationship detected")
    else:
        print("Weak price-volume relationship")
    print()

# 12. PERFORMANCE BENCHMARKING
def performance_benchmarking(df):
    """Benchmark against hypothetical market"""
    print("=== 12. PERFORMANCE BENCHMARKING ANALYTICS ===")
    
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Calculate metrics
    total_return = (1 + df['Daily_Return']).cumprod().iloc[-1] - 1
    annual_return = (1 + total_return) ** (252/len(df)) - 1
    volatility = df['Daily_Return'].std() * np.sqrt(252)
    
    # Assume market returns 8% annually with 15% volatility
    market_annual_return = 0.08
    market_volatility = 0.15
    
    # Calculate tracking error (simplified)
    market_daily_return = market_annual_return / 252
    market_returns = np.random.normal(market_daily_return, market_volatility/np.sqrt(252), len(df['Daily_Return'].dropna()))
    tracking_error = np.std(df['Daily_Return'].dropna() - market_returns) * np.sqrt(252)
    
    # Information ratio
    excess_return = annual_return - market_annual_return
    information_ratio = excess_return / tracking_error if tracking_error > 0 else 0
    
    print(f"Stock annual return: {annual_return:.2%}")
    print(f"Market benchmark return: {market_annual_return:.2%}")
    print(f"Excess return vs market: {excess_return:.2%}")
    print(f"Tracking error: {tracking_error:.2%}")
    print(f"Information ratio: {information_ratio:.2f}")
    
    if annual_return > market_annual_return:
        print("Performance: OUTPERFORMING market")
    else:
        print("Performance: UNDERPERFORMING market")
    print()

def main():
    """Run all analytics examples"""
    print("COMPREHENSIVE BUSINESS ANALYTICS FOR STOCK DATA")
    print("=" * 60)
    print()
    
    # Load data
    df = load_data('stock_data.xlsx')
    
    # Run all analytics examples
    descriptive_analytics(df)
    performance_analytics(df)
    technical_analysis(df)
    risk_analytics(df)
    time_series_analysis(df)
    volatility_analysis(df)
    predictive_analytics(df)
    trading_strategy_analysis(df)
    market_sentiment_analysis(df)
    market_regime_analysis(df)
    correlation_analysis(df)
    performance_benchmarking(df)
    
    print("=" * 60)
    print("ANALYSIS COMPLETE - All 12 analytics types demonstrated")
    print("=" * 60)

if __name__ == "__main__":
    main()
