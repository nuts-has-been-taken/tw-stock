import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def get_comprehensive_financial_data(symbol):
    """
    獲取指定股票的完整財務數據和分析
    
    Parameters:
    symbol (str): 股票代碼，如 '2330.TW'
    
    Returns:
    dict: 包含所有財務數據和計算指標的字典
    """
    
    try:
        # 創建股票對象
        stock = yf.Ticker(symbol)
        
        # 初始化結果字典
        result = {
            'symbol': symbol,
            'basic_info': {},
            'financial_ratios': {},
            'growth_rates': {},
            'cashflow_analysis': {},
            'raw_data': {},
            'data_availability': {},
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 1. 獲取基本信息
        info = stock.info
        basic_metrics = {
            'company_name': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'current_price': info.get('currentPrice', 'N/A'),
            'trailing_eps': info.get('trailingEps', 'N/A'),
            'forward_eps': info.get('forwardEps', 'N/A'),
            'profit_margin': info.get('profitMargins', 'N/A'),
            'gross_margin': info.get('grossMargins', 'N/A'),
            'operating_margin': info.get('operatingMargins', 'N/A'),
            'return_on_assets': info.get('returnOnAssets', 'N/A'),
            'return_on_equity': info.get('returnOnEquity', 'N/A'),
            'revenue_growth': info.get('revenueGrowth', 'N/A'),
            'earnings_growth': info.get('earningsGrowth', 'N/A'),
            'debt_to_equity': info.get('debtToEquity', 'N/A'),
            'current_ratio': info.get('currentRatio', 'N/A'),
            'quick_ratio': info.get('quickRatio', 'N/A')
        }
        result['basic_info'] = basic_metrics
        
        # 2. 獲取財務報表
        income_stmt = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow
        quarterly_income = stock.quarterly_income_stmt
        quarterly_balance = stock.quarterly_balance_sheet
        quarterly_cashflow = stock.quarterly_cashflow
        
        result['raw_data'] = {
            'income_statement_annual': income_stmt,
            'balance_sheet_annual': balance_sheet,
            'cashflow_annual': cashflow,
            'income_statement_quarterly': quarterly_income,
            'balance_sheet_quarterly': quarterly_balance,
            'cashflow_quarterly': quarterly_cashflow
        }
        
        # 3. 數據可用性檢查
        result['data_availability'] = {
            'income_statement': not income_stmt.empty,
            'balance_sheet': not balance_sheet.empty,
            'cashflow': not cashflow.empty,
            'quarterly_income': not quarterly_income.empty,
            'quarterly_balance': not quarterly_balance.empty,
            'quarterly_cashflow': not quarterly_cashflow.empty,
            'basic_info': len(info) > 10,
            'data_years': len(income_stmt.columns) if not income_stmt.empty else 0,
            'quarterly_periods': len(quarterly_income.columns) if not quarterly_income.empty else 0
        }
        
        # 4. 計算財務比率（如果數據可用）
        if not income_stmt.empty:
            try:
                latest_year = income_stmt.columns[0]
                
                # 基本財務數據
                revenue = income_stmt.loc['Total Revenue', latest_year] if 'Total Revenue' in income_stmt.index else None
                gross_profit = income_stmt.loc['Gross Profit', latest_year] if 'Gross Profit' in income_stmt.index else None
                operating_income = income_stmt.loc['Operating Income', latest_year] if 'Operating Income' in income_stmt.index else None
                net_income = income_stmt.loc['Net Income', latest_year] if 'Net Income' in income_stmt.index else None
                basic_eps = income_stmt.loc['Basic EPS', latest_year] if 'Basic EPS' in income_stmt.index else None
                
                # 計算比率
                financial_ratios = {
                    'latest_year': latest_year.strftime('%Y'),
                    'revenue_ntd': revenue,
                    'gross_profit_ntd': gross_profit,
                    'operating_income_ntd': operating_income,
                    'net_income_ntd': net_income,
                    'basic_eps': basic_eps
                }
                
                if revenue and revenue != 0:
                    if gross_profit:
                        financial_ratios['gross_margin_calculated'] = (gross_profit / revenue) * 100
                    if operating_income:
                        financial_ratios['operating_margin_calculated'] = (operating_income / revenue) * 100
                    if net_income:
                        financial_ratios['net_margin_calculated'] = (net_income / revenue) * 100
                
                # 資產負債表相關比率
                if not balance_sheet.empty and net_income:
                    if 'Total Assets' in balance_sheet.index:
                        total_assets = balance_sheet.loc['Total Assets', latest_year]
                        if total_assets and total_assets != 0:
                            financial_ratios['roa_calculated'] = (net_income / total_assets) * 100
                            financial_ratios['total_assets_ntd'] = total_assets
                    
                    if 'Stockholders Equity' in balance_sheet.index:
                        equity = balance_sheet.loc['Stockholders Equity', latest_year]
                        if equity and equity != 0:
                            financial_ratios['roe_calculated'] = (net_income / equity) * 100
                            financial_ratios['stockholders_equity_ntd'] = equity
                    
                    if 'Total Debt' in balance_sheet.index and 'Total Assets' in balance_sheet.index:
                        total_debt = balance_sheet.loc['Total Debt', latest_year]
                        total_assets = balance_sheet.loc['Total Assets', latest_year]
                        if total_assets and total_assets != 0:
                            financial_ratios['debt_ratio_calculated'] = (total_debt / total_assets) * 100
                            financial_ratios['total_debt_ntd'] = total_debt
                
                result['financial_ratios'] = financial_ratios
                
                # 5. 計算成長率
                if income_stmt.shape[1] >= 2:
                    growth_rates = {}
                    
                    # 營收成長率
                    if 'Total Revenue' in income_stmt.index:
                        current_revenue = income_stmt.loc['Total Revenue'].iloc[0]
                        previous_revenue = income_stmt.loc['Total Revenue'].iloc[1]
                        if previous_revenue != 0:
                            growth_rates['revenue_growth_calculated'] = ((current_revenue - previous_revenue) / previous_revenue) * 100
                            growth_rates['current_revenue'] = current_revenue
                            growth_rates['previous_revenue'] = previous_revenue
                    
                    # EPS成長率
                    if 'Basic EPS' in income_stmt.index:
                        current_eps = income_stmt.loc['Basic EPS'].iloc[0]
                        previous_eps = income_stmt.loc['Basic EPS'].iloc[1]
                        if previous_eps != 0:
                            growth_rates['eps_growth_calculated'] = ((current_eps - previous_eps) / previous_eps) * 100
                            growth_rates['current_eps'] = current_eps
                            growth_rates['previous_eps'] = previous_eps
                    
                    # 淨利成長率
                    if 'Net Income' in income_stmt.index:
                        current_ni = income_stmt.loc['Net Income'].iloc[0]
                        previous_ni = income_stmt.loc['Net Income'].iloc[1]
                        if previous_ni != 0:
                            growth_rates['net_income_growth_calculated'] = ((current_ni - previous_ni) / previous_ni) * 100
                            growth_rates['current_net_income'] = current_ni
                            growth_rates['previous_net_income'] = previous_ni
                    
                    result['growth_rates'] = growth_rates
            
            except Exception as e:
                result['calculation_error'] = str(e)
        
        # 6. 現金流分析
        if not cashflow.empty:
            try:
                cashflow_analysis = {}
                latest_year = cashflow.columns[0]
                
                key_items = ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Free Cash Flow']
                for item in key_items:
                    if item in cashflow.index:
                        value = cashflow.loc[item, latest_year]
                        key_name = item.lower().replace(' ', '_')
                        cashflow_analysis[key_name] = value
                
                # 現金流品質分析
                if 'Operating Cash Flow' in cashflow.index and not income_stmt.empty:
                    if 'Net Income' in income_stmt.index:
                        operating_cf = cashflow.loc['Operating Cash Flow', latest_year]
                        net_income = income_stmt.loc['Net Income', latest_year]
                        if net_income != 0:
                            cashflow_analysis['ocf_to_ni_ratio'] = operating_cf / net_income
                
                if 'Free Cash Flow' in cashflow.index and not income_stmt.empty:
                    if 'Net Income' in income_stmt.index:
                        free_cf = cashflow.loc['Free Cash Flow', latest_year]
                        net_income = income_stmt.loc['Net Income', latest_year]
                        if net_income != 0:
                            cashflow_analysis['fcf_to_ni_ratio'] = free_cf / net_income
                
                # 歷史現金流趨勢（如果有多年數據）
                if cashflow.shape[1] >= 3:
                    cashflow_trends = {}
                    for i, year in enumerate(cashflow.columns[:3]):
                        year_key = f'year_{i+1}'
                        cashflow_trends[year_key] = {
                            'year': year.strftime('%Y'),
                            'operating_cf': cashflow.loc['Operating Cash Flow', year] if 'Operating Cash Flow' in cashflow.index else None,
                            'free_cf': cashflow.loc['Free Cash Flow', year] if 'Free Cash Flow' in cashflow.index else None
                        }
                    cashflow_analysis['trends'] = cashflow_trends
                
                result['cashflow_analysis'] = cashflow_analysis
            
            except Exception as e:
                result['cashflow_error'] = str(e)
        
        return result
    
    except Exception as e:
        return {'error': str(e), 'symbol': symbol}

def print_financial_summary(data):
    """
    打印財務數據摘要
    """
    if 'error' in data:
        print(f"錯誤: {data['error']}")
        return
    
    print(f"=== {data['basic_info']['company_name']} ({data['symbol']}) 財務分析 ===")
    print(f"分析時間: {data['analysis_date']}")
    print(f"產業: {data['basic_info']['sector']} - {data['basic_info']['industry']}")
    
    # 基本指標
    if data['basic_info']['market_cap'] != 'N/A':
        print(f"市值: {data['basic_info']['market_cap']/1e12:.2f} 兆")
    if data['basic_info']['current_price'] != 'N/A':
        print(f"當前股價: {data['basic_info']['current_price']}")
    
    # 數據可用性
    print(f"\n--- 數據可用性 ---")
    availability = data['data_availability']
    print(f"年度財務數據: {availability['data_years']} 年")
    print(f"季度財務數據: {availability['quarterly_periods']} 季")
    for key, value in availability.items():
        if isinstance(value, bool):
            print(f"{key}: {'✓' if value else '✗'}")
    
    # 財務比率
    if data['financial_ratios']:
        print(f"\n--- 財務比率 ({data['financial_ratios']['latest_year']}) ---")
        ratios = data['financial_ratios']
        
        if 'revenue_ntd' in ratios and ratios['revenue_ntd']:
            print(f"營收: {ratios['revenue_ntd']/1e12:.2f} 兆")
        if 'net_income_ntd' in ratios and ratios['net_income_ntd']:
            print(f"淨利: {ratios['net_income_ntd']/1e12:.2f} 兆")
        if 'basic_eps' in ratios and ratios['basic_eps']:
            print(f"EPS: {ratios['basic_eps']:.2f}")
        
        if 'gross_margin_calculated' in ratios:
            print(f"毛利率: {ratios['gross_margin_calculated']:.2f}%")
        if 'operating_margin_calculated' in ratios:
            print(f"營業利益率: {ratios['operating_margin_calculated']:.2f}%")
        if 'net_margin_calculated' in ratios:
            print(f"淨利率: {ratios['net_margin_calculated']:.2f}%")
        if 'roa_calculated' in ratios:
            print(f"ROA: {ratios['roa_calculated']:.2f}%")
        if 'roe_calculated' in ratios:
            print(f"ROE: {ratios['roe_calculated']:.2f}%")
        if 'debt_ratio_calculated' in ratios:
            print(f"負債比: {ratios['debt_ratio_calculated']:.2f}%")
    
    # 成長率
    if data['growth_rates']:
        print(f"\n--- 成長率分析 ---")
        growth = data['growth_rates']
        if 'revenue_growth_calculated' in growth:
            print(f"營收成長率: {growth['revenue_growth_calculated']:.2f}%")
        if 'eps_growth_calculated' in growth:
            print(f"EPS成長率: {growth['eps_growth_calculated']:.2f}%")
        if 'net_income_growth_calculated' in growth:
            print(f"淨利成長率: {growth['net_income_growth_calculated']:.2f}%")
    
    # 現金流分析
    if data['cashflow_analysis']:
        print(f"\n--- 現金流分析 ---")
        cf = data['cashflow_analysis']
        if 'operating_cash_flow' in cf:
            print(f"營業現金流: {cf['operating_cash_flow']/1e12:.2f} 兆")
        if 'free_cash_flow' in cf:
            print(f"自由現金流: {cf['free_cash_flow']/1e12:.2f} 兆")
        if 'ocf_to_ni_ratio' in cf:
            print(f"營業現金流/淨利比率: {cf['ocf_to_ni_ratio']:.2f}")
        if 'fcf_to_ni_ratio' in cf:
            print(f"自由現金流/淨利比率: {cf['fcf_to_ni_ratio']:.2f}")

# 測試函數
if __name__ == "__main__":
    print("=== yfinance 台灣股票完整財務分析測試 ===\n")
    
    # 測試台積電
    tsmc_data = get_comprehensive_financial_data("2330.TW")
    print_financial_summary(tsmc_data)
    
    print("\n" + "="*60 + "\n")
    
    # 測試聯發科
    mtk_data = get_comprehensive_financial_data("2454.TW")
    print_financial_summary(mtk_data)