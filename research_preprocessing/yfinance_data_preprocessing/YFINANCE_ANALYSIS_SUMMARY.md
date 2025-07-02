# yfinance 台灣股票財務數據深度分析報告

## 執行摘要

本報告深入分析了 yfinance 對台灣股票市場財務數據的支援情況，通過對台積電(2330.TW)等8檔台灣知名股票的測試，評估各類財務指標的可用性和數據品質。

### 關鍵發現
- **數據可用性**: yfinance 對台灣股票提供了**出色的數據支援**，測試的8檔股票100%成功獲取完整財務數據
- **財務報表完整性**: 損益表、資產負債表、現金流量表數據完整可用
- **時間覆蓋**: 通常提供4-5年年度數據和5-6季季度數據
- **數據更新**: 財務數據及時更新，與台灣上市公司財報發布同步

## 詳細分析結果

### 1. 基本財務指標可用性

| 指標類型 | 直接可用 | 需計算 | 可用性評估 |
|---------|---------|-------|-----------|
| **營收成長率** | ✓ (部分) | ✓ | 🟢 高 - 可直接獲取或通過歷史數據計算 |
| **毛利率** | ✓ | ✓ | 🟢 高 - info中有grossMargins，也可計算驗證 |
| **淨利率** | ✓ | ✓ | 🟢 高 - info中有profitMargins，也可計算驗證 |
| **每股盈餘(EPS)** | ✓ | ✗ | 🟢 高 - trailingEps直接可用 |
| **EPS成長率** | ✓ (部分) | ✓ | 🟢 高 - 可通過歷史EPS計算 |
| **現金流數據** | ✓ | ✗ | 🟢 高 - 營業、投資、融資現金流完整 |
| **負債比** | ✗ | ✓ | 🟡 中 - 需通過資產負債表計算 |
| **ROA** | ✓ | ✓ | 🟢 高 - info中有returnOnAssets |
| **ROE** | ✓ | ✓ | 🟢 高 - info中有returnOnEquity |
| **營業利益率** | ✓ | ✓ | 🟢 高 - info中有operatingMargins |

### 2. 財務報表數據結構

#### 損益表 (Income Statement)
- **年度數據**: 4-5年歷史數據
- **季度數據**: 5-6季歷史數據
- **主要項目**: 
  - Total Revenue ✓
  - Gross Profit ✓
  - Operating Income ✓
  - Net Income ✓
  - Basic EPS ✓
  - Diluted EPS ✓

#### 資產負債表 (Balance Sheet)
- **年度數據**: 4-5年歷史數據
- **季度數據**: 5-6季歷史數據
- **主要項目**:
  - Total Assets ✓
  - Total Debt ✓
  - Stockholders Equity ✓
  - Current Assets ✓
  - Current Liabilities ✓

#### 現金流量表 (Cash Flow)
- **年度數據**: 4-5年歷史數據
- **季度數據**: 5-6季歷史數據
- **主要項目**:
  - Operating Cash Flow ✓
  - Investing Cash Flow ✓
  - Financing Cash Flow ✓
  - Free Cash Flow ✓

### 3. 台積電(2330.TW)實際數據範例

```python
# 基本財務指標 (2024年)
營收: 2.89 兆
淨利: 1.16 兆
EPS: 45.25
毛利率: 56.12%
營業利益率: 45.68%
淨利率: 40.02%
ROA: 17.31%
ROE: 27.29%
負債比: 15.65%

# 成長率分析
營收成長率: 33.89%
EPS成長率: 39.92%
淨利成長率: 36.00%

# 現金流分析
營業現金流: 1.83 兆
自由現金流: 0.86 兆
營業現金流/淨利比率: 1.58
```

### 4. 數據時間範圍和更新頻率

| 數據類型 | 時間範圍 | 更新頻率 |
|---------|---------|---------|
| **股價數據** | 實時/歷史任意範圍 | 實時(交易時間內) |
| **年度財務數據** | 通常4-5年 | 年報發布後 |
| **季度財務數據** | 通常5-6季 | 季報發布後 |
| **基本面指標** | 最新TTM數據 | 財報更新後計算 |

### 5. 多檔台灣股票測試結果

測試8檔台灣知名股票：台積電、鴻海、聯發科、國泰金、台塑、中華電、南亞、台達電

**成功率統計**:
- 基本信息獲取: 8/8 (100%)
- 損益表數據: 8/8 (100%)
- 資產負債表數據: 8/8 (100%)
- 現金流量表數據: 8/8 (100%)
- 季度數據: 8/8 (100%)

## 實用代碼範例

### 基本財務數據獲取
```python
import yfinance as yf

# 創建股票對象
stock = yf.Ticker("2330.TW")

# 獲取基本信息
info = stock.info
print(f"EPS: {info.get('trailingEps')}")
print(f"ROE: {info.get('returnOnEquity')}")
print(f"淨利率: {info.get('profitMargins')}")

# 獲取財務報表
income_stmt = stock.income_stmt
balance_sheet = stock.balance_sheet
cashflow = stock.cashflow
```

### 計算財務比率
```python
# 獲取最新年度數據
latest_year = income_stmt.columns[0]
revenue = income_stmt.loc['Total Revenue', latest_year]
net_income = income_stmt.loc['Net Income', latest_year]

# 計算淨利率
net_margin = (net_income / revenue) * 100
print(f"計算淨利率: {net_margin:.2f}%")

# 計算ROE
total_assets = balance_sheet.loc['Total Assets', latest_year]
equity = balance_sheet.loc['Stockholders Equity', latest_year]
roe = (net_income / equity) * 100
print(f"計算ROE: {roe:.2f}%")
```

### 成長率計算
```python
# 營收成長率
current_revenue = income_stmt.loc['Total Revenue'].iloc[0]
previous_revenue = income_stmt.loc['Total Revenue'].iloc[1]
revenue_growth = ((current_revenue - previous_revenue) / previous_revenue) * 100
print(f"營收成長率: {revenue_growth:.2f}%")

# EPS成長率
current_eps = income_stmt.loc['Basic EPS'].iloc[0]
previous_eps = income_stmt.loc['Basic EPS'].iloc[1]
eps_growth = ((current_eps - previous_eps) / previous_eps) * 100
print(f"EPS成長率: {eps_growth:.2f}%")
```

## 使用建議與最佳實踐

### 1. 數據驗證
```python
# 始終檢查數據可用性
if not stock.income_stmt.empty:
    # 處理財務數據
    pass
else:
    print("財務數據不可用")

# 驗證關鍵數據
info = stock.info
if info.get('trailingEps') and info['trailingEps'] != 'N/A':
    print(f"EPS: {info['trailingEps']}")
```

### 2. 錯誤處理
```python
try:
    stock = yf.Ticker(symbol)
    income_stmt = stock.income_stmt
    
    if not income_stmt.empty:
        # 處理數據
        latest_year = income_stmt.columns[0]
        revenue = income_stmt.loc['Total Revenue', latest_year]
    else:
        print("損益表數據不可用")
        
except Exception as e:
    print(f"獲取數據時發生錯誤: {e}")
```

### 3. 數據品質檢查
```python
# 檢查數據完整性
def check_data_quality(stock):
    checks = {
        'basic_info': len(stock.info) > 10,
        'income_stmt': not stock.income_stmt.empty,
        'balance_sheet': not stock.balance_sheet.empty,
        'cashflow': not stock.cashflow.empty
    }
    
    for check, result in checks.items():
        print(f"{check}: {'✓' if result else '✗'}")
    
    return all(checks.values())
```

## 限制與注意事項

### 1. 數據更新延遲
- 財務報表數據依賴公司財報發布
- 通常有1-3個月的延遲
- 季報數據更新較年報及時

### 2. 數據準確性
- yfinance 數據來源為第三方提供
- 建議與官方財報進行交叉驗證
- 重要決策前應確認數據準確性

### 3. 計算指標差異
- yfinance 提供的比率可能與手動計算略有差異
- 計算方法可能因數據來源而異
- 建議同時使用直接獲取和計算驗證

### 4. 台灣特殊會計準則
- 部分台灣特有的財務項目可能不完整
- 建議結合台灣本地數據源使用

## 結論

yfinance 對台灣股票市場提供了**優秀的數據支援**，能夠滿足大部分財務分析需求：

**優勢**:
- ✅ 數據覆蓋完整 (100%測試股票成功)
- ✅ 財務報表數據詳盡
- ✅ 關鍵指標直接可用
- ✅ 歷史數據充足
- ✅ 使用簡便

**需要注意**:
- ⚠️ 數據更新有延遲
- ⚠️ 需要適當的錯誤處理
- ⚠️ 重要決策前建議數據驗證

**建議使用場景**:
- 🎯 股票篩選和初步分析
- 🎯 財務比率計算和比較
- 🎯 歷史趨勢分析
- 🎯 自動化財務分析系統

總體而言，yfinance 是分析台灣股票財務數據的**優秀工具**，配合適當的使用方法，能夠提供可靠的財務分析基礎。