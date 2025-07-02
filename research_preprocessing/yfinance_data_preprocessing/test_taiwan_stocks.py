import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

print('=== 台灣股票數據可用性比較測試 ===')

taiwan_stocks = {
    '2330.TW': '台積電',
    '2317.TW': '鴻海',
    '2454.TW': '聯發科',
    '2882.TW': '國泰金',
    '1301.TW': '台塑',
    '2412.TW': '中華電',
    '1303.TW': '南亞',
    '2308.TW': '台達電'
}

results = {}

for symbol, name in taiwan_stocks.items():
    print(f'\n--- {name} ({symbol}) ---')
    
    try:
        stock = yf.Ticker(symbol)
        
        # 檢查基本信息
        info = stock.info
        has_basic_info = len(info) > 10
        
        # 檢查財務報表
        has_income_stmt = not stock.income_stmt.empty
        has_balance_sheet = not stock.balance_sheet.empty
        has_cashflow = not stock.cashflow.empty
        has_quarterly = not stock.quarterly_income_stmt.empty
        
        # 記錄結果
        results[symbol] = {
            'name': name,
            'basic_info': has_basic_info,
            'income_statement': has_income_stmt,
            'balance_sheet': has_balance_sheet,
            'cashflow': has_cashflow,
            'quarterly_data': has_quarterly,
            'market_cap': info.get('marketCap', 'N/A'),
            'trailing_eps': info.get('trailingEps', 'N/A'),
            'profit_margin': info.get('profitMargins', 'N/A'),
            'gross_margin': info.get('grossMargins', 'N/A'),
            'roe': info.get('returnOnEquity', 'N/A')
        }
        
        # 顯示數據可用性
        print(f'基本信息: {"✓" if has_basic_info else "✗"}')
        print(f'損益表: {"✓" if has_income_stmt else "✗"}')
        print(f'資產負債表: {"✓" if has_balance_sheet else "✗"}')
        print(f'現金流量表: {"✓" if has_cashflow else "✗"}')
        print(f'季度數據: {"✓" if has_quarterly else "✗"}')
        
        # 顯示關鍵指標
        market_cap = info.get('marketCap')
        if market_cap and market_cap != 'N/A':
            print(f'市值: {market_cap/1e12:.2f} 兆')
        
        trailing_eps = info.get('trailingEps')
        if trailing_eps and trailing_eps != 'N/A':
            print(f'EPS: {trailing_eps:.2f}')
        
        profit_margin = info.get('profitMargins')
        if profit_margin and profit_margin != 'N/A':
            print(f'淨利率: {profit_margin*100:.2f}%')
        
        gross_margin = info.get('grossMargins')
        if gross_margin and gross_margin != 'N/A':
            print(f'毛利率: {gross_margin*100:.2f}%')
        
        roe = info.get('returnOnEquity')
        if roe and roe != 'N/A':
            print(f'ROE: {roe*100:.2f}%')
        
        # 如果有財務報表數據，顯示數據年份範圍
        if has_income_stmt:
            years = stock.income_stmt.columns
            print(f'財務數據年份: {years[-1].year}-{years[0].year} ({len(years)}年)')
        
    except Exception as e:
        print(f'錯誤: {e}')
        results[symbol] = {'name': name, 'error': str(e)}

# 總結統計
print('\n=== 整體數據可用性統計 ===')
successful_stocks = [s for s in results if 'error' not in results[s]]
total_stocks = len(taiwan_stocks)

print(f'成功獲取數據的股票: {len(successful_stocks)}/{total_stocks} ({len(successful_stocks)/total_stocks*100:.0f}%)')

if successful_stocks:
    data_types = ['basic_info', 'income_statement', 'balance_sheet', 'cashflow', 'quarterly_data']
    
    for data_type in data_types:
        count = sum(1 for s in successful_stocks if results[s].get(data_type, False))
        percentage = count / len(successful_stocks) * 100
        print(f'{data_type}: {count}/{len(successful_stocks)} ({percentage:.0f}%)')

# 顯示有完整財務數據的股票
print('\n=== 完整財務數據可用的股票 ===')
complete_stocks = []
for symbol in successful_stocks:
    data = results[symbol]
    if (data.get('income_statement', False) and 
        data.get('balance_sheet', False) and 
        data.get('cashflow', False)):
        complete_stocks.append(symbol)
        print(f'{data["name"]} ({symbol})')

print(f'\n完整財務數據可用股票數: {len(complete_stocks)}/{len(successful_stocks)}')