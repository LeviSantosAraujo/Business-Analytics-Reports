# Business Analytics Dashboard

A comprehensive Python-based business analytics solution for stock market data analysis and reporting, featuring both console-based analytics and an interactive web dashboard.

## 📊 Project Overview

This project provides 12 different types of business analytics for stock market data, with automated report generation in both Excel and text formats, plus professional visualizations. It also includes a Flask-based web application with an interactive dashboard.

## 🚀 Features

### Analytics Modules
1. **Descriptive Analytics** - Basic statistics and data overview
2. **Performance Analytics** - Returns, volatility, and performance metrics
3. **Technical Analytics** - Moving averages, RSI, and trading signals
4. **Risk Analytics** - Value at Risk, drawdown analysis, Sharpe ratio
5. **Time Series Analytics** - Seasonality patterns and trend analysis
6. **Volatility Analytics** - Volatility patterns and clustering analysis
7. **Predictive Analytics** - Moving average crossovers and trend predictions
8. **Trading Strategy Analytics** - Strategy backtesting and performance comparison
9. **Market Sentiment Analytics** - Volume-price relationship analysis
10. **Market Regime Analytics** - Bull/bear market identification
11. **Correlation Analytics** - Price-volume correlation analysis
12. **Performance Benchmarking** - Market comparison and information ratio

### Web Application Features
- **Interactive Dashboard** - Real-time analytics visualization
- **Multiple Pages** - Home, Dashboard, About, Documentation
- **API Endpoints** - RESTful API for analytics data
- **Vercel Deployment** - Serverless-ready for cloud deployment
- **Responsive Design** - Modern, mobile-friendly interface

### Output Formats
- **Excel Reports** - Professional formatted spreadsheets with color coding
- **Text Reports** - Detailed analysis summaries
- **Charts** - High-resolution PNG visualizations
- **Summary Report** - Complete project overview
- **Web Dashboard** - Interactive analytics display

## 📁 Project Structure

```
Business Analytics Reports/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config.py                         # Configuration settings
├── app.py                             # Minimal Flask app (Vercel compatible)
├── app_with_analytics.py              # Flask app with analytics integration
├── comprehensive_analytics.py        # Main analytics script (12 modules, console output)
├── generate_reports.py              # Text + Charts generator (8 modules)
├── generate_excel_reports.py        # Excel reports generator (8 modules)
├── DevicesData.xlsx                  # Sample data file
├── vercel.json                       # Vercel deployment configuration
├── Makefile                          # Build automation
├── templates/                        # HTML templates for web app
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── about.html
│   └── documentation.html
├── static/                           # Static assets
│   ├── css/
│   └── js/
├── reports/                          # Generated reports directory
│   ├── 01_descriptive_analytics.txt
│   ├── 02_performance_analytics.txt
│   ├── 03_technical_analytics.txt
│   ├── 04_risk_analytics.txt
│   ├── 05_time_series_analytics.txt
│   ├── 06_volatility_analytics.txt
│   ├── 07_predictive_analytics.txt
│   ├── 08_trading_strategy_analytics.txt
│   ├── 01_descriptive_analytics.xlsx
│   ├── 02_performance_analytics.xlsx
│   ├── 03_technical_analytics.xlsx
│   ├── 04_risk_analytics.xlsx
│   ├── 05_time_series_analytics.xlsx
│   ├── 06_volatility_analytics.xlsx
│   ├── 07_predictive_analytics.xlsx
│   ├── 08_trading_strategy_analytics.xlsx
│   ├── charts/                       # Generated charts
│   │   ├── 01_descriptive_analytics.png
│   │   ├── 02_performance_analytics.png
│   │   ├── 03_technical_analytics.png
│   │   ├── 04_risk_analytics.png
│   │   ├── 05_time_series_analytics.png
│   │   ├── 06_volatility_analytics.png
│   │   ├── 07_predictive_analytics.png
│   │   └── 08_trading_strategy_analytics.png
│   └── SUMMARY_REPORT.txt
├── .venv/                            # Virtual environment
└── .vscode/                          # VS Code settings
```

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project**
   ```bash
   # If using git
   git clone https://github.com/LeviSantosAraujo/Business-Analytics-Reports.git
   cd "Business Analytics Reports"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python comprehensive_analytics.py
   ```

## 📖 Usage

### Quick Start

#### Console-Based Analytics

1. **Run comprehensive analysis (12 modules, console output)**
   ```bash
   python comprehensive_analytics.py
   ```

2. **Generate text reports and charts (8 modules)**
   ```bash
   python generate_reports.py
   ```

3. **Generate Excel reports (8 modules)**
   ```bash
   python generate_excel_reports.py
   ```

#### Web Application

1. **Run minimal Flask app**
   ```bash
   python app.py
   ```
   Access at: http://localhost:5000

2. **Run Flask app with analytics integration**
   ```bash
   python app_with_analytics.py
   ```
   Access at: http://localhost:5000
   Dashboard at: http://localhost:5000/dashboard

3. **Deploy to Vercel**
   ```bash
   vercel deploy
   ```

### Data Format

The system expects stock data in Excel format with the following structure:
- **Single column** with comma-separated values
- **Format**: `Date,Open,High,Low,Close,Adj Close,Volume`
- **Example**: `2023-01-01,100.00,105.00,99.00,104.50,104.50,1000000`

### Customization

#### Change Data File
Edit the data file path in any script or use environment variables:
```python
# In script
df = load_data('your_data_file.xlsx')

# Or via environment variable
export DATA_FILE="your_data_file.xlsx"
```

#### Modify Analytics
Each analytics function can be customized in the respective script:
- Add new metrics
- Modify calculations
- Change visualization parameters

#### Configuration
Edit `config.py` to customize:
- Analytics parameters (SMA periods, RSI windows, etc.)
- Chart settings (DPI, style, colors)
- Excel formatting (fonts, colors, borders)
- Output directories

#### Excel Styling
Customize colors and formatting in `generate_excel_reports.py`:
```python
# Modify color schemes
title_fill = PatternFill(start_color='2F75B5', end_color='2F75B5', fill_type='solid')
```

## 📊 Analytics Details

### 1. Descriptive Analytics
- **Purpose**: Basic data overview and statistics
- **Metrics**: Trading days, volume, price ranges, basic statistics
- **Output**: Summary statistics + price/volume charts

### 2. Performance Analytics
- **Purpose**: Return and volatility analysis
- **Metrics**: Total return, annualized return, volatility
- **Output**: Performance metrics + cumulative returns chart

### 3. Technical Analytics
- **Purpose**: Technical indicator analysis
- **Metrics**: Moving averages, RSI, trading signals
- **Output**: Technical indicators + signal charts

### 4. Risk Analytics
- **Purpose**: Risk assessment and metrics
- **Metrics**: VaR, maximum drawdown, Sharpe ratio
- **Output**: Risk metrics + distribution charts

### 5. Time Series Analytics
- **Purpose**: Seasonality and trend analysis
- **Metrics**: Monthly patterns, yearly trends
- **Output**: Seasonal analysis + trend charts

### 6. Volatility Analytics
- **Purpose**: Volatility pattern analysis
- **Metrics**: Rolling volatility, volatility clustering
- **Output**: Volatility metrics + volatility charts

### 7. Predictive Analytics
- **Purpose**: Trend prediction using technical analysis
- **Metrics**: Moving average crossovers, trend signals
- **Output**: Predictions + signal charts

### 8. Trading Strategy Analytics
- **Purpose**: Strategy backtesting and comparison
- **Metrics**: Strategy returns vs buy & hold
- **Output**: Performance comparison + strategy charts

### 9. Market Sentiment Analytics
- **Purpose**: Volume-price relationship analysis
- **Metrics**: Volume ratios, high-volume day returns, up/down volume
- **Output**: Sentiment indicators (bullish/bearish/neutral)

### 10. Market Regime Analytics
- **Purpose**: Identify bull/bear market periods
- **Metrics**: 200-day SMA analysis, regime percentages
- **Output**: Current market regime identification

### 11. Correlation Analytics
- **Purpose**: Price-volume correlation analysis
- **Metrics**: Price-volume correlation, autocorrelation, return patterns
- **Output**: Correlation coefficients and relationship strength

### 12. Performance Benchmarking
- **Purpose**: Benchmark against hypothetical market
- **Metrics**: Excess return, tracking error, information ratio
- **Output**: Performance vs market comparison

## 🎨 Excel Report Features

### Professional Formatting
- **Color-coded headers** with professional blue theme
- **Conditional formatting** for performance indicators
- **Proper number formatting** (currency, percentages, decimals)
- **Bordered tables** with clean alignment
- **Centered headers** with bold formatting

### Color Coding
- 🟢 **Green**: Positive performance, bullish signals, good metrics
- 🔴 **Red**: Negative performance, bearish signals, high risk
- 🟡 **Yellow/Orange**: Neutral or cautionary indicators
- 🔵 **Blue**: Headers and professional styling

## 📈 Chart Features

### High-Quality Visualizations
- **300 DPI resolution** for professional presentations
- **Professional styling** with grids and legends
- **Multiple chart types**: Line charts, bar charts, histograms
- **Color-coded indicators** for easy interpretation
- **Proper axis formatting** with percentage and currency labels

## 🔧 Configuration

### Settings File (`config.py`)
The project uses a centralized configuration file (`config.py`) for all settings:

```python
# Data settings
DATA_FILE = 'DevicesData.xlsx'
OUTPUT_DIR = 'reports'

# Analytics settings
RISK_FREE_RATE = 0.02
TRADING_DAYS_PER_YEAR = 252
SMA_SHORT_PERIOD = 20
SMA_MEDIUM_PERIOD = 50
SMA_LONG_PERIOD = 200
RSI_PERIOD = 14
VOLATILITY_WINDOW = 30

# Chart settings
CHART_DPI = 300
CHART_STYLE = "seaborn-v0_8"
CHART_FIGURE_SIZE = (12, 8)

# Excel formatting
EXCEL_FONT_NAME = "Calibri"
EXCEL_HEADER_COLOR = "2F75B5"
EXCEL_POSITIVE_COLOR = "C6E0B4"
EXCEL_NEGATIVE_COLOR = "F8CBAD"
```

### Environment Variables
```bash
# Data configuration
export DATA_FILE="your_data_file.xlsx"
export OUTPUT_DIR="/path/to/reports"

# Analytics configuration
export RISK_FREE_RATE="0.02"
export CHART_DPI="300"

# Report generation
export GENERATE_EXCEL="true"
export GENERATE_CHARTS="true"
export GENERATE_TEXT_REPORTS="true"
```

### Validate Configuration
```bash
python config.py
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

2. **FileNotFoundError**
   - Ensure data file exists in the correct location
   - Check file path in the script

3. **Excel Permission Errors**
   - Close any Excel applications
   - Check file permissions

4. **Memory Issues**
   - For large datasets, process data in chunks
   - Increase system RAM or use cloud processing

### Debug Mode
Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Code formatting
black *.py
flake8 *.py
```

### Adding New Analytics
1. Create new function in appropriate script (`comprehensive_analytics.py` for console, `generate_reports.py` for charts/text, `generate_excel_reports.py` for Excel)
2. Follow existing naming conventions
3. Add proper documentation
4. Include error handling
5. Update README if needed
6. Add configuration options to `config.py` if needed

### Web Application Development
- Templates are in the `templates/` directory
- Static assets (CSS/JS) are in the `static/` directory
- Flask routes are defined in `app.py` and `app_with_analytics.py`
- For Vercel deployment, ensure the `handler()` function is defined

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

### Getting Help
- **Documentation**: Check this README file
- **Issues**: Report bugs via GitHub issues
- **Questions**: Contact the development team

### Resources
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions)

## 🔄 Version History

### v2.0.0 (Current)
- Expanded from 8 to 12 analytics modules
- Added Flask web application with interactive dashboard
- Added Vercel deployment support
- Centralized configuration system (`config.py`)
- Enhanced Excel report generation with professional formatting
- Chart generation with high-quality visualizations
- API endpoints for analytics data
- Comprehensive documentation

### v1.0.0
- Initial release with 8 analytics modules
- Excel report generation with professional formatting
- Chart generation with high-quality visualizations
- Comprehensive documentation

### Future Updates
- [ ] Real-time data integration
- [ ] Additional technical indicators
- [ ] Machine learning predictions
- [ ] Enhanced web dashboard with interactive charts
- [ ] API authentication and rate limiting
- [ ] Database integration for historical data

## 📊 Sample Output

### Excel Report Preview
```
DESCRIPTIVE ANALYTICS REPORT
=======================================
Metric              Value
Data Period         1980-03-18 to 2023-07-10
Total Trading Days  10,919
Average Volume      18,464,946
Price Range         $1.61 - $164.46
```

### Analytics Summary
- **Total Return**: 3,647%
- **Annualized Return**: 8.72%
- **Current Signal**: Bullish
- **Risk Level**: High Volatility
- **Strategy Performance**: Buy & Hold outperforms

---

**Generated with ❤️ using Python, pandas, matplotlib, and openpyxl**
