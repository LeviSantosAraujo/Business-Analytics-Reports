"""
Business Analytics Dashboard Setup Script
Comprehensive stock market data analysis and reporting tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="business-analytics-dashboard",
    version="1.0.0",
    author="Business Analytics Team",
    author_email="analytics@company.com",
    description="Comprehensive Python-based business analytics solution for stock market data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/company/business-analytics-dashboard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "black>=24.0.0",
            "flake8>=7.0.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "business-analytics=comprehensive_analytics:main",
            "generate-reports=generate_reports:main",
            "excel-reports=generate_excel_reports:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.xlsx", "*.csv", "*.md"],
    },
    keywords="business analytics, stock market, financial analysis, reporting, excel, charts",
    project_urls={
        "Bug Reports": "https://github.com/company/business-analytics-dashboard/issues",
        "Source": "https://github.com/company/business-analytics-dashboard",
        "Documentation": "https://github.com/company/business-analytics-dashboard/wiki",
    },
)
