# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research-focused repository for Taiwan stock market data analysis using Jupyter notebooks. The project explores various market factors and their correlation with stock prices through data science methodologies.

## Common Development Commands

### Environment Setup
```bash
# Install required dependencies
pip3 install yfinance pandas requests matplotlib scikit-learn jupyter beautifulsoup4 selenium transformers torch

# Start Jupyter notebook server
jupyter notebook

# Navigate to research notebooks
cd stock_experiment
```

### Git Workflow
```bash
# Create research branch
git checkout -b research-topic-name

# Common commit pattern (using conventional commits with emojis)
git commit -m ":construction: Add new research analysis"
git commit -m ":bug: Fix data collection issue"
git commit -m ":memo: Update experiment documentation"
```

## Architecture and Structure

### Research-Oriented Design
- **Primary Tool**: Jupyter notebooks for interactive data analysis
- **Language**: Python with data science libraries
- **Data Sources**: Yahoo Finance (yfinance), Taiwan Stock Exchange (TWSE) APIs
- **Research Workflow**: Data Collection → Preprocessing → Analysis → Visualization → Correlation Analysis

### Key Components

#### Core Libraries
- `yfinance` - Stock price data from Yahoo Finance
- `pandas` - Data manipulation and analysis
- `requests` - Web scraping from TWSE APIs
- `matplotlib` - Data visualization
- `sklearn.preprocessing.StandardScaler` - Data standardization
- `beautifulsoup4` + `selenium` - Web scraping for news analysis
- `transformers` - NLP models for sentiment analysis

#### Directory Structure
```
stock_experiment/          # Research notebooks directory
├── major_investors_movements.ipynb  # ✅ Completed: Institutional investor analysis
├── JPY_interest.ipynb              # ✅ Completed: JPY interest rate research  
├── finance_news.ipynb              # 🚧 In progress: News sentiment analysis
└── unemployment_rate.ipynb         # 🚧 Cancelled: Unemployment analysis
```

### Data Architecture Patterns

#### Stock Data Functions
- `get_stock_from_yf(stock_code, start_date, end_date)` - Downloads stock data and calculates cumulative growth
- `data_pretreatment(mi_df)` - Standardizes and processes institutional investor data
- `correlation(stock_df, mi_df)` - Calculates correlation coefficients

#### Major Investors Data Pipeline
- `get_mi_movement_from_twse(start_date, end_date, stock_code)` - Scrapes TWSE institutional data
- `save_mi_movement_to_csv(df_dict)` - Saves data to CSV for future use
- `read_mi_movement_from_csv(file_path, start_date, end_date)` - Reads cached data

#### Visualization
- `graph_analysis(yf_df, mi_df)` - Creates comparative plots of stock prices vs institutional movements

### Research Methodology

#### Data Standardization Process
1. Raw institutional trading data → StandardScaler normalization
2. Apply cumulative sum with 0.006 weight factor
3. Create weighted combination: Foreign (70%) + Investment Trust (20%) + Self-Dealer (10%)

#### Analysis Focus Areas
- **Foreign Investors (外資)**: Major market influence, high correlation with stock prices
- **Investment Trusts (投信)**: Often shows negative correlation
- **Self-Dealers (自營商)**: Minimal correlation with price movements
- **Combined Analysis**: Weighted institutional impact assessment

## Important Notes

### Data Limitations
- TWSE data availability starts from 2012-05-02
- Format changes occurred after 2018-01-02 (recommended start date)
- Data collection can take ~22 minutes per stock for full historical range

### Development Workflow
1. **Research Phase**: Create individual notebooks for market factor hypotheses
2. **Data Collection**: Use TWSE APIs and yfinance for data gathering  
3. **Analysis**: Perform correlation analysis and visualization
4. **Future Automation**: Successful research functions will be moved to automation_scripts

### Planned Automation
- Daily data updates via cron jobs
- Automated correlation analysis across multiple stocks
- Integration with automation_scripts directory (referenced but not yet implemented)

### Research Languages
- Primary documentation and analysis are in Traditional Chinese
- Code comments and function names use English
- Research findings documented in Chinese within notebooks
