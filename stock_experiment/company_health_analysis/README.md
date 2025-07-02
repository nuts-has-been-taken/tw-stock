# 📊 公司財務健康度分析模組

這是一個專為台灣股市設計的綜合財務健康度分析工具，支援**產業別評分調整**功能。

## 🎯 核心功能

### 1. **多維度財務分析**
- 🏆 **盈利能力** (40% 權重): 營收成長率、毛利率、淨利率、ROE、ROA
- 💰 **每股指標** (25% 權重): EPS、EPS成長率、每股淨值
- 💸 **現金流** (20% 權重): 營運現金流、自由現金流、現金流品質
- 🏗️ **財務結構** (15% 權重): 負債比、流動比率、利息保障倍數

### 2. **產業別智能調整**
支援五大產業專用評分標準：
- 🔬 **科技業**: 台積電、聯發科等 (提高獲利能力權重)
- 🏦 **金融業**: 富邦金、國泰金等 (調整負債比標準)
- 🏭 **製造業**: 台塑、中鋼等 (重視現金流穩定)
- 🛒 **零售業**: 統一超、全家等 (平衡各項指標)
- ⚡ **公用事業**: 中華電、台灣大等 (重視穩定性)

### 3. **視覺化分析**
- 📈 健康度雷達圖
- 📊 多公司比較圖表
- 🏭 產業分析對比

## 📁 檔案結構

```
company_health_analysis/
├── __init__.py                           # 模組初始化
├── company_health_analysis.ipynb         # 主要分析筆記本
├── industry_financial_analysis.py        # 產業財務特性分析器
├── industry_scoring_recommendations.py   # 產業評分標準調整
├── 台灣產業財務分析總結報告.md           # 完整分析報告
└── README.md                            # 使用說明 (本檔案)
```

## 🚀 快速開始

### 基本使用
```python
# 導入模組
from industry_financial_analysis import IndustryFinancialAnalyzer
from industry_scoring_recommendations import IndustryScoringRecommendations

# 單一公司分析
financial_data = get_company_financial_data("2330.TW")
health_metrics = calculate_health_metrics(financial_data)
health_scores = calculate_health_score(health_metrics, use_industry_adjustment=True)

# 顯示結果
display_health_summary(health_metrics, health_scores)
create_health_radar_chart(health_metrics, health_scores)
```

### 多公司比較
```python
# 多公司健康度比較
comparison_stocks = ["2330.TW", "2317.TW", "2454.TW", "2881.TW"]
results = compare_multiple_companies(comparison_stocks)
```

### 產業調整功能
```python
# 比較通用 vs 產業調整評分
generic_scores, industry_scores = compare_scoring_methods("2330.TW")
```

## 🎯 產業調整邏輯

### 科技業調整 (如台積電)
```python
權重調整: 盈利能力 40%→45%, 現金流 20%→15%
評分提升: 毛利率門檻 40%→50%, ROE門檻 20%→25%
原因: 技術優勢是核心競爭力，現金流波動屬正常
```

### 金融業調整 (如富邦金)
```python
權重調整: 盈利能力 40%→30%, 每股指標 25%→35%, 現金流 20%→10%
評分調整: ROA門檻 12%→1.5%, 負債比容忍 30%→90%
原因: 金融業天生高負債，ROA較低屬正常
```

### 製造業調整 (如台塑)
```python
權重調整: 盈利能力 40%→30%, 現金流 20%→35%
評分降低: 毛利率門檻 40%→20%, 成長率門檻 15%→8%
原因: 週期性產業，現金管理更重要
```

## 📊 評分等級

| 總分範圍 | 健康度等級 | 說明 |
|----------|------------|------|
| 80-100分 | 優秀 (Excellent) | 財務狀況優異，值得投資 |
| 60-79分  | 良好 (Good) | 財務穩健，可考慮投資 |
| 40-59分  | 普通 (Average) | 財務一般，需謹慎評估 |
| 0-39分   | 警示 (Warning) | 財務風險較高，不建議投資 |

## 🔬 進階功能

### 產業特性分析
```python
# 查看產業財務特性
profile = industry_analyzer.get_industry_profile('科技業')
print(profile['characteristics'])
```

### 自定義評分標準
```python
# 取得產業專用評分標準
criteria = industry_scorer.get_industry_scoring('金融業')
weights = industry_scorer.get_industry_weights('金融業')
```

### 評分差異分析
```python
# 分析評分方法差異
comparison = industry_scorer.compare_scoring_difference(
    stock_code="2330.TW", 
    generic_vs_industry=True
)
```

## 📈 應用場景

1. **投資篩選**: 快速識別財務健康的投資標的
2. **風險控制**: 監控投資組合中的財務風險
3. **同業比較**: 產業內公司競爭力評估
4. **定期監控**: 追蹤公司健康度變化趨勢

## 🛠️ 系統要求

```python
# 必要套件
pip3 install yfinance pandas numpy matplotlib seaborn
```

## 📝 更新日誌

### v1.0.0 (Current)
- ✅ 基礎健康度分析功能
- ✅ 五大產業別調整機制
- ✅ 視覺化分析工具
- ✅ 多公司比較功能
- ✅ 完整錯誤處理機制

### 🔮 未來規劃
- 📊 趨勢分析功能
- 🚨 財務預警系統
- 🔄 自動化報告生成
- 📱 互動式儀表板

## 💡 使用建議

1. **首次使用**: 建議先執行單一公司分析熟悉系統
2. **產業調整**: 預設開啟產業調整功能，獲得更準確評分
3. **定期更新**: 建議每季更新財務數據
4. **謹慎投資**: 評分僅供參考，投資決策需綜合考量多項因素

---

**開發者**: Claude Code  
**最後更新**: 2024年  
**授權**: MIT License