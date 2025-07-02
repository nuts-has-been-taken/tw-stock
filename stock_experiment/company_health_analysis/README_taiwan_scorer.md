# 台灣行業財務健康度評分系統

## 📋 概述

本系統提供基於台灣股市特性的行業別財務健康度評分功能，支援13個主要行業的客製化評分標準和權重配置。

## 🏗️ 架構設計

### 核心檔案
- `taiwan_industry_scoring_standards.json` - 評分標準配置檔案
- `taiwan_industry_scorer.py` - 評分系統核心類別
- `README_taiwan_scorer.md` - 使用說明文件

### JSON 結構
```json
{
  "metadata": {...},           // 版本資訊
  "industry_mapping": {...},   // yfinance到台灣行業的映射
  "industry_weights": {...},   // 各行業權重配置
  "scoring_criteria": {...},   // 各行業評分標準
  "typical_companies": {...}   // 各行業代表公司
}
```

## 🏭 支援的行業分類

### 完整支援的13個行業：
1. **科技業** - 台積電、聯發科、廣達等
2. **金融業** - 富邦金、國泰金、兆豐金等  
3. **原物料業** - 台塑、南亞、中鋼等
4. **工業** - 製造業、機械業等
5. **消費循環業** - 汽車、家電、服飾等
6. **民生消費業** - 統一超、統一、全家等
7. **醫療保健業** - 醫藥、醫材等
8. **公用事業** - 電力、瓦斯、水利等
9. **通訊服務業** - 電信、媒體等
10. **能源業** - 石油、天然氣等
11. **不動產業** - 建設、不動產等
12. **運輸物流業** - 航運、物流等
13. **觀光餐飲業** - 觀光、餐飲服務等

## 🎯 評分維度與權重

### 四大評分維度：
1. **盈利能力** (Profitability) - 營收成長率、毛利率、淨利率、ROA、ROE
2. **每股指標** (Per Share) - EPS、EPS成長率、每股淨值
3. **現金流** (Cash Flow) - 營運現金流、自由現金流、現金流對淨利比
4. **財務結構** (Financial Structure) - 負債比、流動比率、利息保障倍數

### 行業別權重差異範例：
```python
科技業: {盈利能力: 45%, 每股指標: 25%, 現金流: 15%, 財務結構: 15%}
金融業: {盈利能力: 35%, 每股指標: 30%, 現金流: 10%, 財務結構: 25%}
原物料業: {盈利能力: 30%, 每股指標: 20%, 現金流: 30%, 財務結構: 20%}
```

## 💻 使用方法

### 基本使用
```python
from taiwan_industry_scorer import TaiwanIndustryScorer

# 初始化評分器
scorer = TaiwanIndustryScorer()

# 準備財務指標數據
metrics = {
    'revenue_growth_rate': 12.5,  # 營收成長率 (%)
    'gross_margin': 55.0,         # 毛利率 (%)
    'net_margin': 22.0,           # 淨利率 (%)
    'roa': 15.0,                  # ROA (%)
    'roe': 20.0,                  # ROE (%)
    'eps': 18.5,                  # EPS
    'eps_growth': 15.0,           # EPS成長率 (%)
    'debt_ratio': 25.0,           # 負債比 (%)
    'current_ratio': 2.1,         # 流動比率
    'ocf_to_net_income': 1.2      # 現金流對淨利比
}

# 計算行業別評分
scores = scorer.calculate_industry_score(metrics, 'Technology')

# 顯示結果
print(f"總分: {scores['total_score']:.1f}")
print(f"等級: {scores['health_grade']}")
print(f"使用行業: {scores['taiwan_industry']}")
```

### 進階功能
```python
# 取得特定行業資訊
tech_info = scorer.get_industry_info('科技業')
print(tech_info['weights'])
print(tech_info['description'])

# 單一指標評分
score, grade = scorer.score_metric(55.0, 'gross_margin', '科技業')
print(f"毛利率評分: {score}分 ({grade})")

# 重新載入設定（修改JSON後）
scorer.reload_standards()

# 取得支援的行業列表
industries = scorer.get_supported_industries()

# 取得行業典型公司
companies = scorer.get_typical_companies('科技業')
```

## ⚙️ 自訂評分標準

### 修改權重配置
編輯 `taiwan_industry_scoring_standards.json` 檔案中的 `industry_weights` 部分：

```json
"科技業": {
  "profitability": 0.50,        // 盈利能力權重調整為50%
  "per_share": 0.25,
  "cash_flow": 0.10,            // 現金流權重調降為10%
  "financial_structure": 0.15,
  "description": "重視盈利能力..."
}
```

### 修改評分標準
編輯 `scoring_criteria` 部分：

```json
"科技業": {
  "gross_margin": {
    "excellent": 55,    // 優秀標準調整為55%
    "good": 45,
    "average": 35,
    "poor": 25,
    "unit": "%"
  }
}
```

### 新增行業
1. 在 `industry_mapping.taiwan_sectors` 新增行業名稱
2. 在 `industry_weights` 新增權重配置
3. 在 `scoring_criteria` 新增評分標準
4. 在 `typical_companies` 新增代表公司（可選）

## 📊 評分等級說明

- **優秀 (Excellent)**: 80-100分
- **良好 (Good)**: 60-79分  
- **普通 (Average)**: 40-59分
- **警示 (Warning)**: 0-39分

## 🔄 與現有系統整合

### 替換現有評分函數
```python
# 原始函數
def calculate_health_score(metrics, use_industry_adjustment=True):
    # 原始實作...
    
# 新的實作方式
def calculate_health_score_v2(metrics, yfinance_sector):
    scorer = TaiwanIndustryScorer()
    return scorer.calculate_industry_score(metrics, yfinance_sector)
```

### 在 Jupyter Notebook 中使用
```python
# 在 company_health_analysis.ipynb 中
from company_health_analysis.taiwan_industry_scorer import TaiwanIndustryScorer

# 替換原有的評分邏輯
scorer = TaiwanIndustryScorer()
health_scores = scorer.calculate_industry_score(health_metrics, info.get('sector', 'Unknown'))
```

## 🛠️ 維護與更新

### 版本控制
JSON檔案中包含版本資訊，修改時請更新：
```json
"metadata": {
  "version": "1.1",
  "created_date": "2024-12-19",
  "last_modified": "2024-12-20"
}
```

### 效能優化
- 評分器初始化時載入JSON，避免重複讀取
- 使用 `reload_standards()` 僅在檔案更新時重新載入
- 快取常用的評分結果（如需要）

## 🔍 錯誤處理

系統會自動處理以下錯誤情況：
- JSON檔案不存在或格式錯誤
- 不支援的行業（自動使用通用標準）
- 缺少的指標數據（自動略過或使用預設值）
- 無效的數值輸入

## 📈 未來擴展

1. **動態權重調整** - 根據市場環境自動調整權重
2. **趨勢分析** - 加入時間序列分析
3. **基準比較** - 與同業或大盤比較
4. **預警系統** - 財務惡化早期警示
5. **機器學習** - 基於歷史數據優化評分標準

## 📞 支援

如需協助或有改進建議，請聯繫開發團隊或在專案中提出Issue。