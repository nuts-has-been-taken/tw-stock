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
- **Modular Structure**: Reusable components with standardized interfaces
- **Industry-Specific Analysis**: Customized financial scoring for 13 Taiwan industry sectors

### Key Components

#### Core Libraries
- `yfinance` - Stock price data from Yahoo Finance
- `pandas` - Data manipulation and analysis
- `requests` - Web scraping from TWSE APIs
- `matplotlib` - Data visualization
- `sklearn.preprocessing.StandardScaler` - Data standardization
- `beautifulsoup4` + `selenium` - Web scraping for news analysis
- `transformers` - NLP models for sentiment analysis

#### Enhanced Directory Structure
```
tw-stock/
├── stock_experiment/          # Research notebooks directory
│   ├── major_investors_movements.ipynb  # ✅ Completed: Institutional investor analysis
│   ├── JPY_interest.ipynb              # ✅ Completed: JPY interest rate research  
│   ├── company_health_analysis.ipynb   # ✅ Completed: Financial health scoring
│   ├── taiwan_etf_analysis.ipynb       # ✅ Completed: ETF constituent analysis
│   ├── taiwan_etf_scraper.py           # ✅ Completed: ETF data scraper
│   ├── test_etf_scraper.py             # ✅ Completed: ETF scraper testing
│   ├── finance_news.ipynb              # 🚧 In progress: News sentiment analysis
│   ├── unemployment_rate.ipynb         # ❌ Cancelled: Unemployment analysis
│   └── company_health_analysis/        # Financial scoring system
│       ├── taiwan_industry_scorer.py    # Industry-specific scoring engine
│       ├── taiwan_industry_scoring_standards.json  # Scoring configurations
│       └── README_taiwan_scorer.md      # Scoring system documentation
│
├── research_preprocessing/    # Data preprocessing tools
│   ├── yfinance_data_preprocessing/     # yfinance tools and analysis
│   │   ├── yfinance_taiwan_analysis.ipynb    # Deep analysis notebook
│   │   ├── yfinance_complete_analysis.py     # Complete analysis module
│   │   ├── test_taiwan_stocks.py             # Quick testing script
│   │   └── YFINANCE_ANALYSIS_SUMMARY.md      # Analysis summary report
│   └── README.md
│
├── data/                       # Data storage directory
│   ├── etf_data/              # ETF constituent and weight data
│   │   ├── etf_list.json           # Taiwan ETF list
│   │   ├── etf_constituents.json   # ETF constituent details
│   │   └── all_etf_constituents.csv # Combined ETF data in CSV format
│   └── mi_movements_csv/       # Major investor movement data
│
└── README.md                  # Enhanced project documentation
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

#### Financial Health Scoring System
- `TaiwanIndustryScorer` - Industry-specific financial health scoring class
- `calculate_industry_score(metrics, yfinance_sector)` - Calculates weighted health scores
- `get_industry_info(taiwan_industry)` - Retrieves industry-specific configurations
- `score_metric(value, metric_name, industry)` - Scores individual financial metrics

#### yfinance Data Processing
- `get_comprehensive_financial_data(symbol)` - Complete financial data extraction
- `analyze_taiwan_stock_data(symbols)` - Batch analysis of Taiwan stocks
- `validate_data_quality(stock_data)` - Data quality assessment

#### ETF Analysis System
- `TaiwanETFScraper` - Taiwan ETF data collection and analysis class
- `get_taiwan_etf_list()` - Retrieves comprehensive Taiwan ETF list
- `get_etf_constituents_mock(etf_code)` - Gets ETF constituent stocks and weights
- `collect_all_etf_data(max_etfs, delay)` - Batch collection of ETF data
- `save_to_csv()` - Saves ETF data to CSV format for analysis
- `analyze_etf_overlap(etf1, etf2)` - Analyzes overlap between ETFs
- `calculate_stock_frequency(etf_constituents)` - Stock frequency across ETFs

#### Visualization
- `graph_analysis(yf_df, mi_df)` - Creates comparative plots of stock prices vs institutional movements
- Financial health scoring visualization and reporting

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
2. **Data Preprocessing**: Develop and test data collection tools in research_preprocessing/
3. **Data Collection**: Use TWSE APIs and yfinance for data gathering  
4. **Analysis**: Perform correlation analysis and visualization
5. **Modularization**: Extract successful functions into reusable modules
6. **Future Automation**: Successful research functions will be moved to automation_scripts

### Planned Automation
- Daily data updates via cron jobs
- Automated correlation analysis across multiple stocks
- Integration with automation_scripts directory (referenced but not yet implemented)
- Automated financial health scoring for portfolio monitoring
- Real-time institutional investor movement alerts
- Multi-factor correlation analysis dashboard

### Research Languages
- Primary documentation and analysis are in Traditional Chinese
- Code comments and function names use English
- Research findings documented in Chinese within notebooks

## New Components and Tools

### Financial Health Scoring System
```python
from company_health_analysis.taiwan_industry_scorer import TaiwanIndustryScorer

# Initialize scorer
scorer = TaiwanIndustryScorer()

# Calculate health score
health_metrics = {
    'revenue_growth_rate': 12.5,
    'gross_margin': 55.0,
    'net_margin': 22.0,
    'roa': 15.0,
    'roe': 20.0,
    'eps': 18.5,
    'eps_growth': 15.0,
    'debt_ratio': 25.0,
    'current_ratio': 2.1,
    'ocf_to_net_income': 1.2
}

scores = scorer.calculate_industry_score(health_metrics, 'Technology')
print(f"Total Score: {scores['total_score']:.1f}")
print(f"Health Grade: {scores['health_grade']}")
```

### yfinance Taiwan Analysis Tools
```python
from research_preprocessing.yfinance_data_preprocessing.yfinance_complete_analysis import get_comprehensive_financial_data

# Get complete financial data for Taiwan stocks
financial_data = get_comprehensive_financial_data('2330.TW')
print(f"EPS: {financial_data['eps']}")
print(f"ROE: {financial_data['roe']}")
```

### Industry-Specific Configurations
- **13 Taiwan Industry Sectors**: Technology, Finance, Materials, Industrial, Consumer Cyclical, Consumer Defensive, Healthcare, Utilities, Communication Services, Energy, Real Estate, Transportation, Tourism & Hospitality
- **Custom Weights**: Each industry has specific weights for Profitability, Per Share metrics, Cash Flow, and Financial Structure
- **Scoring Standards**: Industry-adjusted benchmarks for financial metrics

### Data Preprocessing Best Practices
1. **Data Validation**: Always validate data quality before analysis
2. **Error Handling**: Implement comprehensive error handling for data collection
3. **Caching**: Use CSV caching for expensive data collection operations
4. **Documentation**: Document data sources, limitations, and processing steps

### Testing and Quality Assurance
```python
# Test Taiwan stock data availability
from research_preprocessing.yfinance_data_preprocessing.test_taiwan_stocks import test_multiple_stocks

# Test multiple Taiwan stocks
test_results = test_multiple_stocks(['2330.TW', '2317.TW', '2454.TW'])
print(f"Success rate: {test_results['success_rate']}")
```

### ETF Analysis Usage Examples

#### Basic ETF Data Collection
```python
from taiwan_etf_scraper import TaiwanETFScraper

# Initialize ETF scraper
scraper = TaiwanETFScraper()

# Get Taiwan ETF list
etf_list = scraper.get_taiwan_etf_list()
print(f"Found {len(etf_list)} ETFs")

# Collect ETF constituent data
etf_data = scraper.collect_all_etf_data(max_etfs=10)

# Save to CSV files
etf_df, all_df = scraper.save_to_csv()

# Print analysis report
scraper.print_summary_report()
```

#### ETF Overlap Analysis
```python
# Analyze overlap between two ETFs
def analyze_etf_overlap(etf1_constituents, etf2_constituents):
    etf1_stocks = {stock['stock_code'] for stock in etf1_constituents}
    etf2_stocks = {stock['stock_code'] for stock in etf2_constituents}
    
    overlap_stocks = etf1_stocks & etf2_stocks
    overlap_ratio = len(overlap_stocks) / len(etf1_stocks | etf2_stocks)
    
    return {
        'overlap_ratio': overlap_ratio,
        'overlap_stocks': list(overlap_stocks)
    }

# Example: Compare 0050 and 0056 overlap
overlap_result = analyze_etf_overlap(
    etf_data['0050']['constituents'],
    etf_data['0056']['constituents']
)
print(f"Overlap ratio: {overlap_result['overlap_ratio']:.2%}")
```

#### Stock Frequency Analysis
```python
# Calculate stock frequency across ETFs
def calculate_stock_frequency(etf_constituents):
    stock_frequency = {}
    
    for etf_code, data in etf_constituents.items():
        for constituent in data['constituents']:
            stock_code = constituent['stock_code']
            if stock_code not in stock_frequency:
                stock_frequency[stock_code] = {
                    'name': constituent['stock_name'],
                    'count': 0,
                    'total_weight': 0
                }
            
            stock_frequency[stock_code]['count'] += 1
            stock_frequency[stock_code]['total_weight'] += constituent['weight']
    
    return stock_frequency

# Find most popular stocks across ETFs
stock_freq = calculate_stock_frequency(etf_data)
popular_stocks = sorted(stock_freq.items(), key=lambda x: x[1]['count'], reverse=True)
print("Top 5 most frequent stocks:")
for stock_code, info in popular_stocks[:5]:
    print(f"  {stock_code} {info['name']}: appears in {info['count']} ETFs")
```
