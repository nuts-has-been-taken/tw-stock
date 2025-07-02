# 📈 台灣股市數據分析研究

這個 repository 專注於台灣股票市場的數據分析研究，目的是探討各種市場因素對股價的影響，並建立系統化的分析工具。

## 🎯 專案目標

- **市場因子研究**: 分析三大法人、日圓利率、新聞情緒等因素對股價的影響
- **工具化開發**: 建立可重複使用的分析模組和前處理工具
- **財務健康度評估**: 開發台灣股市特定的行業財務評分系統
- **自動化分析**: 將成功的研究方法轉化為自動化分析工具

## 📁 專案結構

```
tw-stock/
├── 📊 stock_experiment/           # 研究主題實驗
│   ├── major_investors_movements.ipynb    # ✅ 三大法人研究
│   ├── JPY_interest.ipynb                # ✅ 日圓利率研究
│   ├── company_health_analysis.ipynb     # ✅ 公司財務健康度
│   ├── finance_news.ipynb               # 🚧 新聞情緒分析
│   ├── unemployment_rate.ipynb          # ❌ 失業率研究(暫停)
│   └── company_health_analysis/         # 財務評分系統
│       ├── taiwan_industry_scorer.py    # 行業評分核心
│       └── taiwan_industry_scoring_standards.json
│
├── 🔧 research_preprocessing/     # 研究前處理工具
│   ├── yfinance_data_preprocessing/     # yfinance 工具
│   │   ├── yfinance_taiwan_analysis.ipynb
│   │   ├── yfinance_complete_analysis.py
│   │   └── YFINANCE_ANALYSIS_SUMMARY.md
│   └── README.md
│
├── 📋 CLAUDE.md                  # AI 開發指南
└── 📖 README.md                  # 專案說明文件
```

## 🔬 研究主題

### ✅ 已完成的研究

#### 1. 三大法人買賣超分析 (`major_investors_movements`)
- **研究內容**: 外資、投信、自營商對股價影響
- **核心發現**: 外資影響最大，投信常呈負相關
- **權重配置**: 外資70% + 投信20% + 自營商10%
- **數據來源**: 台灣證交所 API

#### 2. 日圓利率關聯研究 (`JPY_interest`)
- **研究內容**: 日本利率政策與台股關聯性
- **分析範圍**: 全球金融市場互動關係
- **應用價值**: 國際資金流向判斷

#### 3. 公司財務健康度分析 (`company_health_analysis`)
- **評分系統**: 支援13個台灣主要行業
- **評分維度**: 盈利能力、每股指標、現金流、財務結構
- **行業調整**: 各行業權重客製化配置
- **應用範圍**: 個股基本面評估

### 🚧 進行中的研究

#### 新聞情緒分析 (`finance_news`)
- **目標**: 分析財經新聞對股價的影響
- **技術**: NLP + 情緒分析模型
- **狀態**: 開發中

### 📝 計劃中的研究

- 大戶籌碼對股價影響
- 散戶指標研究  
- 市場新聞對行情影響

## 🛠️ 技術架構

### 核心技術棧
- **語言**: Python
- **數據科學**: pandas, numpy, scikit-learn
- **視覺化**: matplotlib, plotly
- **金融數據**: yfinance, 台灣證交所 API
- **NLP**: transformers, beautifulsoup4, selenium
- **環境**: Jupyter Notebook

### 數據處理流程
1. **數據收集** → 多源數據整合
2. **前處理** → 標準化與清理
3. **特徵工程** → 指標計算與轉換
4. **分析建模** → 相關性分析與預測
5. **視覺化** → 結果呈現與洞察

## 🚀 快速開始

### 環境設置
```bash
# 安裝依賴套件
pip3 install yfinance pandas requests matplotlib scikit-learn jupyter beautifulsoup4 selenium transformers torch

# 啟動 Jupyter Notebook
jupyter notebook

# 進入研究目錄
cd stock_experiment
```

### 基本使用

#### 三大法人分析
```python
# 載入三大法人數據
from major_investors_movements import get_mi_movement_from_twse, correlation

# 獲取台積電數據
mi_data = get_mi_movement_from_twse('2018-01-02', '2024-01-01', '2330')
correlation_result = correlation(stock_data, mi_data)
```

#### 財務健康度評分
```python
# 使用行業評分系統
from company_health_analysis.taiwan_industry_scorer import TaiwanIndustryScorer

scorer = TaiwanIndustryScorer()
health_score = scorer.calculate_industry_score(financial_metrics, 'Technology')
print(f"健康度評分: {health_score['total_score']}")
```

## 📊 研究成果

### 重要發現
- **外資影響力**: 與股價相關性達 70%+ 
- **投信反向指標**: 常呈現負相關特徵
- **行業差異**: 不同行業財務指標權重差異顯著
- **時間序列**: 累積效應比單日效應更具預測性

### 實際應用
- 投資決策輔助工具
- 風險評估模型
- 市場情緒指標
- 自動化交易策略參考

## 🔄 開發流程

### 研究階段
1. **假設提出** → 確立研究方向
2. **數據驗證** → 前處理工具開發
3. **實驗分析** → Jupyter Notebook 實作  
4. **結果驗證** → 相關性分析與視覺化

### 工具化階段
5. **模組抽取** → 將成功函數模組化
6. **標準化** → 統一介面與錯誤處理
7. **自動化** → 整合至 automation_scripts

## 🤝 貢獻指南

### 新增研究主題
1. 在 `stock_experiment/` 建立新的 `.ipynb` 檔案
2. 遵循既有的研究模板和命名規範
3. 完成後更新 README.md 和 CLAUDE.md

### 前處理工具開發
1. 在 `research_preprocessing/` 建立新的數據源工具
2. 提供完整的測試和文檔
3. 確保與現有工具整合

### 程式碼規範
- 使用英文函數命名和註解
- 研究文檔使用繁體中文
- 遵循 PEP 8 程式碼風格

## 📈 未來規劃

### 短期目標 (1-3個月)
- [ ] 完成新聞情緒分析研究
- [ ] 建立自動化數據更新機制
- [ ] 開發即時監控儀表板

### 中期目標 (3-6個月)  
- [ ] 整合多因子分析模型
- [ ] 建立預警系統
- [ ] 開發 Web 應用介面

### 長期目標 (6個月以上)
- [ ] 機器學習預測模型
- [ ] 即時交易策略系統
- [ ] 開源社群建設

## 📞 聯絡資訊

如有問題或建議，歡迎提出 Issue 或 Pull Request。

---

**最後更新**: 2025-07-02  
**專案狀態**: 積極開發中  
**授權**: 研究用途
