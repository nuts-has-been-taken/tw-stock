# 📈 yfinance 台灣股票數據前處理工具

這個模組專門用於 yfinance 數據來源的前處理工作，包含完整的可用性分析、測試工具和標準化數據獲取函數。

## 🎯 模組目的

1. **驗證 yfinance 對台灣股票的支援程度**
2. **建立標準化的數據獲取函數**
3. **提供可重複使用的財務分析工具**
4. **為正式研究項目提供可靠的數據基礎**

## 📁 檔案說明

### 📊 分析和研究
- **`yfinance_taiwan_analysis.ipynb`** - 深度分析筆記本
  - yfinance 對台灣股票的完整功能測試
  - 各種財務指標的可用性分析
  - 數據結構和時間範圍探索
  - 實際範例和最佳實踐

### 🧪 測試工具
- **`test_taiwan_stocks.py`** - 快速測試腳本
  - 批量測試多檔台灣股票的數據可用性
  - 生成數據可用性統計報告
  - 適合定期檢查數據來源狀態

### 🔧 核心模組
- **`yfinance_complete_analysis.py`** - 完整分析工具模組
  - 標準化的數據獲取函數
  - 財務比率計算功能
  - 成長率分析工具
  - 現金流分析功能
  - 完整的錯誤處理機制

### 📋 總結報告
- **`YFINANCE_ANALYSIS_SUMMARY.md`** - 完整分析總結
  - 所有測試結果的彙整
  - 關鍵發現和限制說明
  - 使用建議和最佳實踐
  - 實用代碼範例

## 🚀 快速開始

### 基本使用範例

```python
# 導入核心模組
from yfinance_complete_analysis import get_comprehensive_financial_data

# 獲取單一股票完整財務數據
data = get_comprehensive_financial_data("2330.TW")

# 檢查數據可用性
if 'error' not in data:
    print(f"公司: {data['basic_info']['company_name']}")
    print(f"產業: {data['basic_info']['sector']}")
    
    # 顯示財務比率
    for ratio, value in data['financial_ratios'].items():
        print(f"{ratio}: {value:.2f}%")
else:
    print(f"錯誤: {data['error']}")
```

### 批量測試範例

```bash
# 執行台灣股票數據可用性測試
python3 test_taiwan_stocks.py
```

## 📊 主要功能

### 1. 數據可用性檢查
- ✅ 基本股票資訊（100% 可用）
- ✅ 損益表數據（100% 可用）
- ✅ 資產負債表數據（100% 可用）
- ✅ 現金流量表數據（100% 可用）
- ✅ 季度財務數據（100% 可用）

### 2. 財務指標計算
- 📈 **盈利能力**: 毛利率、淨利率、營業利益率、ROA、ROE
- 📊 **成長分析**: 營收成長率、EPS成長率、淨利成長率
- 💰 **現金流**: 營業現金流、自由現金流、現金流品質比率
- 🏗️ **財務結構**: 負債比、流動比率、利息保障倍數

### 3. 支援的台灣股票範圍
測試涵蓋主要產業：
- 🔬 **科技業**: 台積電(2330)、聯發科(2454)、台達電(2308)
- 🏭 **製造業**: 鴻海(2317)、台塑(1301)、南亞(1303)
- 🏦 **金融業**: 國泰金(2882)
- ⚡ **公用事業**: 中華電(2412)

## 💡 使用建議

### 1. 在正式研究中使用
```python
# 在 stock_experiment 中的研究筆記本裡
import sys
sys.path.append('../research_preprocessing/yfinance_data_preprocessing')
from yfinance_complete_analysis import get_comprehensive_financial_data

# 然後就可以使用標準化的數據獲取功能
```

### 2. 數據驗證最佳實踐
- 始終檢查數據可用性
- 實作適當的錯誤處理
- 驗證計算結果的合理性
- 定期更新數據來源測試

### 3. 效能優化
- 使用快取避免重複獲取相同數據
- 批量處理多檔股票時添加延遲
- 定期檢查 yfinance 更新狀況

## 🔗 相關研究項目

這個前處理工具已被用於：

1. **`stock_experiment/company_health_analysis/`**
   - 公司財務健康度綜合分析
   - 產業別評分調整機制

2. **`stock_experiment/major_investors_movements/`**
   - 結合 yfinance 股價數據進行相關性分析

## 📈 數據更新頻率

- **股價數據**: 實時（交易時間內）
- **年度財務數據**: 年報發布後（通常有1-3個月延遲）
- **季度財務數據**: 季報發布後（較年報及時）
- **基本面指標**: 財報更新後重新計算

## ⚠️ 使用限制

1. **數據延遲**: 財務報表數據依賴公司財報發布
2. **準確性**: 建議與官方財報交叉驗證重要數據
3. **台灣特殊項目**: 部分台灣特有會計項目可能不完整
4. **更新頻率**: 第三方數據來源，可能有服務中斷

## 🛠️ 系統需求

```bash
# 必要套件
pip3 install yfinance pandas numpy matplotlib warnings
```

---

**開發完成日期**: 2025-07-02  
**測試股票數量**: 8檔台灣主要股票  
**數據可用性**: 100% 成功率  
**用途**: 支援台灣股市研究的 yfinance 數據前處理