# 📊 研究前處理工具

這個資料夾包含各種研究項目的數據前處理工具和分析模組。

## 🎯 目的

在正式進行股市研究之前，需要先：
1. **驗證數據來源可用性** - 確認各數據源能提供所需指標
2. **建立數據獲取工具** - 開發標準化的數據收集函數
3. **測試數據品質** - 驗證數據完整性和準確性
4. **建立預處理模組** - 為正式研究提供可重複使用的工具

## 📁 資料夾結構

```
research_preprocessing/
├── README.md                    # 總說明文件
├── yfinance_data_preprocessing/ # yfinance 數據前處理工具
│   ├── yfinance_taiwan_analysis.ipynb    # 深度分析筆記本
│   ├── test_taiwan_stocks.py             # 快速測試腳本
│   ├── yfinance_complete_analysis.py     # 完整分析模組
│   └── YFINANCE_ANALYSIS_SUMMARY.md      # 分析總結報告
└── [其他數據源前處理工具...]
```

## 🔄 與正式研究的關係

前處理工具 → 正式研究項目的流程：

1. **前處理階段**（本資料夾）：
   - 數據來源可行性分析
   - 工具模組開發和測試
   - 數據品質驗證

2. **正式研究階段**（`stock_experiment/`）：
   - 使用前處理工具進行具體研究
   - 針對特定假設進行分析
   - 產出研究結果和結論

## 🛠️ 使用方式

### 新增數據來源前處理

1. 創建新的子資料夾：`mkdir new_data_source_preprocessing`
2. 開發數據獲取和測試工具
3. 完成驗證後，在正式研究中使用

### 模組重複使用

前處理工具可以被多個研究項目重複使用：

```python
# 在正式研究中導入前處理模組
import sys
sys.path.append('../research_preprocessing/yfinance_data_preprocessing')
from yfinance_complete_analysis import get_comprehensive_financial_data
```

## 📝 開發準則

1. **標準化**：所有前處理工具都應該有統一的接口和錯誤處理
2. **文檔化**：每個工具都要有完整的使用說明和範例
3. **測試覆蓋**：確保工具在各種情況下都能正常運作
4. **模組化**：設計可重複使用的獨立模組

---

**建立日期**: 2025-07-02  
**用途**: 支援台灣股市研究的數據前處理工作