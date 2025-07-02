# 台灣各產業財務健康度評估差異分析
# Industry-Specific Financial Health Analysis for Taiwan Market

import pandas as pd
import numpy as np

class IndustryFinancialAnalyzer:
    """
    針對不同產業的財務健康度評估分析器
    """
    
    def __init__(self):
        # 定義各產業的典型財務特性與評分標準
        self.industry_profiles = {
            "科技業": {
                "description": "半導體、電子零組件、資訊硬體等高科技產業",
                "typical_companies": ["台積電(2330)", "聯發科(2454)", "廣達(2382)", "大立光(3008)"],
                "characteristics": {
                    "毛利率": {
                        "range": "40-60%",
                        "typical": 50,
                        "explanation": "高技術門檻、專利保護與品牌價值",
                        "scoring": {
                            "excellent": 45, "good": 35, "average": 25, "poor": 15
                        }
                    },
                    "淨利率": {
                        "range": "15-25%", 
                        "typical": 20,
                        "explanation": "高研發投入但產品附加價值高",
                        "scoring": {
                            "excellent": 20, "good": 15, "average": 10, "poor": 5
                        }
                    },
                    "負債比": {
                        "range": "15-35%",
                        "typical": 25,
                        "explanation": "現金充裕，財務結構保守",
                        "scoring": {
                            "excellent": 25, "good": 35, "average": 45, "poor": 55
                        }
                    },
                    "ROE": {
                        "range": "15-30%",
                        "typical": 22,
                        "explanation": "高技術壁壘帶來穩定高回報",
                        "scoring": {
                            "excellent": 20, "good": 15, "average": 10, "poor": 5
                        }
                    },
                    "ROA": {
                        "range": "8-18%",
                        "typical": 13,
                        "explanation": "資產使用效率較高",
                        "scoring": {
                            "excellent": 12, "good": 8, "average": 5, "poor": 2
                        }
                    },
                    "營收成長率": {
                        "range": "0-25%",
                        "typical": 12,
                        "explanation": "週期性強，景氣敏感度高",
                        "scoring": {
                            "excellent": 15, "good": 8, "average": 3, "poor": -5
                        }
                    }
                },
                "weight_adjustments": {
                    "profitability": 0.45,  # 提高盈利能力權重
                    "per_share": 0.25,
                    "cash_flow": 0.15,     # 降低現金流權重
                    "financial_structure": 0.15
                }
            },
            
            "金融業": {
                "description": "銀行、保險、證券等金融服務業",
                "typical_companies": ["富邦金(2881)", "國泰金(2882)", "中信金(2891)", "玉山金(2884)"],
                "characteristics": {
                    "毛利率": {
                        "range": "N/A",
                        "typical": None,
                        "explanation": "金融業無毛利率概念，以利差為主",
                        "scoring": None
                    },
                    "淨利率": {
                        "range": "25-45%",
                        "typical": 35,
                        "explanation": "利息收入扣除利息支出後的淨利差",
                        "scoring": {
                            "excellent": 35, "good": 25, "average": 15, "poor": 10
                        }
                    },
                    "負債比": {
                        "range": "85-95%",
                        "typical": 90,
                        "explanation": "存款為主要負債，屬正常營運模式",
                        "scoring": {
                            "excellent": 92, "good": 89, "average": 85, "poor": 80
                        }
                    },
                    "ROE": {
                        "range": "8-16%",
                        "typical": 12,
                        "explanation": "穩定但成長性有限",
                        "scoring": {
                            "excellent": 15, "good": 12, "average": 8, "poor": 5
                        }
                    },
                    "ROA": {
                        "range": "0.6-1.8%",
                        "typical": 1.2,
                        "explanation": "資產規模龐大，報酬率相對較低",
                        "scoring": {
                            "excellent": 1.5, "good": 1.0, "average": 0.7, "poor": 0.4
                        }
                    },
                    "營收成長率": {
                        "range": "3-10%",
                        "typical": 6,
                        "explanation": "穩定成長，受利率環境影響",
                        "scoring": {
                            "excellent": 10, "good": 6, "average": 3, "poor": 0
                        }
                    }
                },
                "weight_adjustments": {
                    "profitability": 0.35,
                    "per_share": 0.30,     # 提高每股指標權重
                    "cash_flow": 0.10,     # 大幅降低現金流權重
                    "financial_structure": 0.25  # 提高財務結構權重
                }
            },
            
            "傳統製造業": {
                "description": "石化、鋼鐵、水泥、塑膠等傳統製造業",
                "typical_companies": ["台塑(1301)", "南亞(1303)", "中鋼(2002)", "台泥(1101)"],
                "characteristics": {
                    "毛利率": {
                        "range": "8-25%",
                        "typical": 16,
                        "explanation": "競爭激烈，受原物料價格影響大",
                        "scoring": {
                            "excellent": 20, "good": 15, "average": 10, "poor": 5
                        }
                    },
                    "淨利率": {
                        "range": "2-12%",
                        "typical": 7,
                        "explanation": "成本控制為關鍵競爭力",
                        "scoring": {
                            "excellent": 10, "good": 6, "average": 3, "poor": 1
                        }
                    },
                    "負債比": {
                        "range": "35-65%",
                        "typical": 50,
                        "explanation": "資本密集，需要大量資金投入",
                        "scoring": {
                            "excellent": 35, "good": 45, "average": 55, "poor": 65
                        }
                    },
                    "ROE": {
                        "range": "4-15%",
                        "typical": 9,
                        "explanation": "週期性強，獲利波動大",
                        "scoring": {
                            "excellent": 12, "good": 8, "average": 5, "poor": 2
                        }
                    },
                    "ROA": {
                        "range": "2-10%",
                        "typical": 6,
                        "explanation": "資產周轉率較低",
                        "scoring": {
                            "excellent": 8, "good": 5, "average": 3, "poor": 1
                        }
                    },
                    "營收成長率": {
                        "range": "-10-15%",
                        "typical": 3,
                        "explanation": "高度週期性，受景氣循環影響",
                        "scoring": {
                            "excellent": 10, "good": 5, "average": 0, "poor": -10
                        }
                    }
                },
                "weight_adjustments": {
                    "profitability": 0.35,
                    "per_share": 0.20,
                    "cash_flow": 0.30,     # 提高現金流權重
                    "financial_structure": 0.15
                }
            },
            
            "零售業": {
                "description": "百貨、超市、連鎖通路等零售服務業",
                "typical_companies": ["統一超(2912)", "全家(5903)", "統一(1216)", "遠百(2903)"],
                "characteristics": {
                    "毛利率": {
                        "range": "20-40%",
                        "typical": 30,
                        "explanation": "通路服務費與自有品牌貢獻",
                        "scoring": {
                            "excellent": 35, "good": 28, "average": 22, "poor": 15
                        }
                    },
                    "淨利率": {
                        "range": "2-10%",
                        "typical": 6,
                        "explanation": "人事與租金成本高",
                        "scoring": {
                            "excellent": 8, "good": 5, "average": 3, "poor": 1
                        }
                    },
                    "負債比": {
                        "range": "25-55%",
                        "typical": 40,
                        "explanation": "應付帳款週轉快",
                        "scoring": {
                            "excellent": 30, "good": 40, "average": 50, "poor": 60
                        }
                    },
                    "ROE": {
                        "range": "10-25%",
                        "typical": 17,
                        "explanation": "資產周轉率高",
                        "scoring": {
                            "excellent": 20, "good": 15, "average": 10, "poor": 5
                        }
                    },
                    "ROA": {
                        "range": "6-18%",
                        "typical": 12,
                        "explanation": "坪效管理為關鍵",
                        "scoring": {
                            "excellent": 15, "good": 10, "average": 6, "poor": 3
                        }
                    },
                    "營收成長率": {
                        "range": "2-12%",
                        "typical": 7,
                        "explanation": "穩定成長，受消費力影響",
                        "scoring": {
                            "excellent": 10, "good": 6, "average": 3, "poor": 0
                        }
                    }
                },
                "weight_adjustments": {
                    "profitability": 0.30,
                    "per_share": 0.25,
                    "cash_flow": 0.25,     # 提高現金流權重
                    "financial_structure": 0.20   # 提高財務結構權重
                }
            },
            
            "公用事業": {
                "description": "電信、電力、瓦斯等公用事業",
                "typical_companies": ["中華電(2412)", "台灣大(3045)", "遠傳(4904)", "大台北瓦斯(9908)"],
                "characteristics": {
                    "毛利率": {
                        "range": "25-55%",
                        "typical": 40,
                        "explanation": "穩定的服務費用收入",
                        "scoring": {
                            "excellent": 50, "good": 40, "average": 30, "poor": 20
                        }
                    },
                    "淨利率": {
                        "range": "8-20%",
                        "typical": 14,
                        "explanation": "受管制定價，獲利穩定",
                        "scoring": {
                            "excellent": 18, "good": 14, "average": 10, "poor": 6
                        }
                    },
                    "負債比": {
                        "range": "20-50%",
                        "typical": 35,
                        "explanation": "穩定現金流支撐適度負債",
                        "scoring": {
                            "excellent": 25, "good": 35, "average": 45, "poor": 55
                        }
                    },
                    "ROE": {
                        "range": "6-18%",
                        "typical": 12,
                        "explanation": "穩定但成長性有限",
                        "scoring": {
                            "excellent": 15, "good": 12, "average": 8, "poor": 5
                        }
                    },
                    "ROA": {
                        "range": "2-12%",
                        "typical": 7,
                        "explanation": "資產密集但使用效率穩定",
                        "scoring": {
                            "excellent": 10, "good": 7, "average": 4, "poor": 2
                        }
                    },
                    "營收成長率": {
                        "range": "0-8%",
                        "typical": 4,
                        "explanation": "成長性低但穩定",
                        "scoring": {
                            "excellent": 6, "good": 4, "average": 2, "poor": 0
                        }
                    }
                },
                "weight_adjustments": {
                    "profitability": 0.30,
                    "per_share": 0.25,
                    "cash_flow": 0.20,
                    "financial_structure": 0.25   # 提高財務結構權重
                }
            }
        }
    
    def get_industry_profile(self, industry_name):
        """獲取特定產業的財務特性檔案"""
        return self.industry_profiles.get(industry_name, None)
    
    def compare_industries(self):
        """比較各產業的財務特性差異"""
        comparison_data = []
        
        for industry, profile in self.industry_profiles.items():
            if industry == "金融業":  # 金融業結構特殊，單獨處理
                comparison_data.append({
                    "產業": industry,
                    "典型毛利率": "N/A",
                    "典型淨利率": f"{profile['characteristics']['淨利率']['typical']}%",
                    "典型負債比": f"{profile['characteristics']['負債比']['typical']}%",
                    "典型ROE": f"{profile['characteristics']['ROE']['typical']}%",
                    "典型ROA": f"{profile['characteristics']['ROA']['typical']}%",
                    "典型營收成長": f"{profile['characteristics']['營收成長率']['typical']}%",
                    "主要特色": "高負債比為正常，重視資本效率"
                })
            else:
                comparison_data.append({
                    "產業": industry,
                    "典型毛利率": f"{profile['characteristics']['毛利率']['typical']}%",
                    "典型淨利率": f"{profile['characteristics']['淨利率']['typical']}%",
                    "典型負債比": f"{profile['characteristics']['負債比']['typical']}%",
                    "典型ROE": f"{profile['characteristics']['ROE']['typical']}%",
                    "典型ROA": f"{profile['characteristics']['ROA']['typical']}%",
                    "典型營收成長": f"{profile['characteristics']['營收成長率']['typical']}%",
                    "主要特色": self.get_industry_feature(industry)
                })
        
        return pd.DataFrame(comparison_data)
    
    def get_industry_feature(self, industry):
        """獲取產業主要特色"""
        features = {
            "科技業": "高毛利高成長，週期性強",
            "傳統製造業": "低毛利週期性，重視成本控制",
            "零售業": "重視周轉率與現金流管理",
            "公用事業": "穩定收益，成長性有限"
        }
        return features.get(industry, "")
    
    def get_industry_specific_scoring(self, industry_name, metric_name):
        """獲取特定產業的評分標準"""
        profile = self.get_industry_profile(industry_name)
        if profile and metric_name in profile['characteristics']:
            return profile['characteristics'][metric_name].get('scoring', None)
        return None
    
    def get_industry_weights(self, industry_name):
        """獲取特定產業的權重配置"""
        profile = self.get_industry_profile(industry_name)
        if profile:
            return profile.get('weight_adjustments', {
                "profitability": 0.40,
                "per_share": 0.25,
                "cash_flow": 0.20,
                "financial_structure": 0.15
            })
        return None
    
    def generate_industry_report(self):
        """生成完整的產業分析報告"""
        report = []
        report.append("🏭 台灣股市各產業財務健康度評估差異分析報告")
        report.append("=" * 80)
        report.append("")
        
        for industry, profile in self.industry_profiles.items():
            report.append(f"📊 {industry}")
            report.append(f"   描述: {profile['description']}")
            report.append(f"   代表企業: {', '.join(profile['typical_companies'])}")
            report.append("")
            
            report.append("   💰 財務特性分析:")
            for metric, data in profile['characteristics'].items():
                if data['typical'] is not None:
                    report.append(f"     • {metric}: {data['range']} (典型值: {data['typical']}%)")
                    report.append(f"       {data['explanation']}")
                else:
                    report.append(f"     • {metric}: {data['explanation']}")
                report.append("")
            
            report.append("   ⚖️ 建議權重配置:")
            weights = profile['weight_adjustments']
            report.append(f"     • 盈利能力: {weights['profitability']*100:.0f}%")
            report.append(f"     • 每股指標: {weights['per_share']*100:.0f}%")
            report.append(f"     • 現金流: {weights['cash_flow']*100:.0f}%")
            report.append(f"     • 財務結構: {weights['financial_structure']*100:.0f}%")
            report.append("")
            report.append("-" * 60)
            report.append("")
        
        return "\n".join(report)


def main():
    """主程式：展示產業分析功能"""
    analyzer = IndustryFinancialAnalyzer()
    
    # 生成完整報告
    print(analyzer.generate_industry_report())
    
    # 產業比較表格
    print("\n📈 各產業典型財務指標比較表")
    print("=" * 100)
    comparison_df = analyzer.compare_industries()
    print(comparison_df.to_string(index=False))
    
    # 權重配置比較
    print("\n⚖️ 各產業建議權重配置比較")
    print("=" * 60)
    print(f"{'產業':<10} {'盈利能力':<8} {'每股指標':<8} {'現金流':<8} {'財務結構':<8}")
    print("-" * 60)
    
    for industry in analyzer.industry_profiles.keys():
        weights = analyzer.get_industry_weights(industry)
        print(f"{industry:<10} {weights['profitability']*100:>6.0f}%   "
              f"{weights['per_share']*100:>6.0f}%   "
              f"{weights['cash_flow']*100:>6.0f}%   "
              f"{weights['financial_structure']*100:>6.0f}%")


if __name__ == "__main__":
    main()