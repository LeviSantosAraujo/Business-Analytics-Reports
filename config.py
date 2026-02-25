"""
Business Analytics Dashboard Configuration
Centralized settings for analytics and reporting
"""

import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"

# Data Configuration
DEFAULT_DATA_FILE = "DevicesData.xlsx"
DATA_FILE = os.environ.get("DATA_FILE", DEFAULT_DATA_FILE)
DATA_PATH = DATA_DIR / DATA_FILE

# Report Configuration
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", str(REPORTS_DIR))
CHART_OUTPUT_DIR = os.environ.get("CHART_OUTPUT_DIR", str(CHARTS_DIR))

# Analytics Configuration
RISK_FREE_RATE = float(os.environ.get("RISK_FREE_RATE", "0.02"))  # 2% default
TRADING_DAYS_PER_YEAR = 252

# Technical Analysis Parameters
SMA_SHORT_PERIOD = 20
SMA_MEDIUM_PERIOD = 50
SMA_LONG_PERIOD = 200
RSI_PERIOD = 14
VOLATILITY_WINDOW = 30

# Chart Configuration
CHART_DPI = int(os.environ.get("CHART_DPI", "300"))
CHART_STYLE = "seaborn-v0_8"
CHART_FIGURE_SIZE = (12, 8)
CHART_LINE_WIDTH = 2
CHART_GRID_ALPHA = 0.3

# Excel Configuration
EXCEL_FONT_NAME = "Calibri"
EXCEL_HEADER_FONT_SIZE = 12
EXCEL_TITLE_FONT_SIZE = 14
EXCEL_DATA_FONT_SIZE = 10

# Excel Color Scheme
EXCEL_HEADER_COLOR = "2F75B5"  # Professional blue
EXCEL_TITLE_COLOR = "DDEBF7"   # Light blue
EXCEL_DATA_COLOR = "FFFFFF"    # White
EXCEL_NUMBER_COLOR = "F2F2F2"  # Light gray

# Conditional Formatting Colors
EXCEL_POSITIVE_COLOR = "C6E0B4"  # Light green
EXCEL_NEGATIVE_COLOR = "F8CBAD"   # Light orange
EXCEL_NEUTRAL_COLOR = "FFEB9C"    # Light yellow
EXCEL_WARNING_COLOR = "E74C3C"    # Red
EXCEL_SUCCESS_COLOR = "70AD47"    # Green

# Report Configuration
GENERATE_EXCEL = os.environ.get("GENERATE_EXCEL", "true").lower() == "true"
GENERATE_CHARTS = os.environ.get("GENERATE_CHARTS", "true").lower() == "true"
GENERATE_TEXT_REPORTS = os.environ.get("GENERATE_TEXT_REPORTS", "true").lower() == "true"

# Performance Configuration
ENABLE_CACHING = os.environ.get("ENABLE_CACHING", "false").lower() == "true"
MAX_MEMORY_USAGE = os.environ.get("MAX_MEMORY_USAGE", "1GB")  # For large datasets

# Logging Configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation Rules
MIN_DATA_POINTS = 100  # Minimum data points for reliable analysis
MAX_MISSING_PERCENTAGE = 0.1  # Maximum 10% missing data allowed

# Business Rules
DEFAULT_PORTFOLIO_WEIGHT = 0.20  # 20% default portfolio weight
BENCHMARK_ANNUAL_RETURN = 0.08   # 8% market benchmark
BENCHMARK_VOLATILITY = 0.15      # 15% market volatility

# API Configuration (for future extensions)
API_TIMEOUT = 30  # seconds
API_RETRY_ATTEMPTS = 3
RATE_LIMIT_DELAY = 1  # seconds between requests

# Email Configuration (for report distribution)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

# Security Configuration
ENABLE_ENCRYPTION = os.environ.get("ENABLE_ENCRYPTION", "false").lower() == "true"
DATA_RETENTION_DAYS = int(os.environ.get("DATA_RETENTION_DAYS", "365"))

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [REPORTS_DIR, CHARTS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories
ensure_directories()

# Configuration Validation
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check data file exists
    if not DATA_PATH.exists():
        errors.append(f"Data file not found: {DATA_PATH}")
    
    # Validate numeric ranges
    if not 0 <= RISK_FREE_RATE <= 1:
        errors.append("RISK_FREE_RATE must be between 0 and 1")
    
    if TRADING_DAYS_PER_YEAR <= 0:
        errors.append("TRADING_DAYS_PER_YEAR must be positive")
    
    if CHART_DPI <= 0:
        errors.append("CHART_DPI must be positive")
    
    # Validate technical analysis periods
    if SMA_SHORT_PERIOD >= SMA_MEDIUM_PERIOD >= SMA_LONG_PERIOD:
        errors.append("SMA periods must be in ascending order")
    
    if errors:
        raise ValueError("Configuration validation failed:\n" + "\n".join(errors))
    
    return True

# Print configuration summary
def print_config():
    """Print current configuration settings"""
    print("=" * 60)
    print("BUSINESS ANALYTICS DASHBOARD CONFIGURATION")
    print("=" * 60)
    print(f"Data File: {DATA_PATH}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Risk-Free Rate: {RISK_FREE_RATE:.2%}")
    print(f"Chart DPI: {CHART_DPI}")
    print(f"Generate Excel: {GENERATE_EXCEL}")
    print(f"Generate Charts: {GENERATE_CHARTS}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        validate_config()
        print_config()
        print("✓ Configuration is valid")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
