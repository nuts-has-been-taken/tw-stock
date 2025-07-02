# 台灣各產業財務健康度評分標準調整建議
# Industry-Specific Scoring Standards for Taiwan Stock Market

import pandas as pd
import numpy as np

class IndustryScoringRecommendations:
    """
    針對不同產業的評分標準調整建議
    """
    
    def __init__(self):
        # 原始通用評分標準 (基準)
        self.generic_scoring = {
            'revenue_growth_rate': {'excellent': 15, 'good': 8, 'average': 3, 'poor': -5},
            'gross_margin': {'excellent': 40, 'good': 25, 'average': 15, 'poor': 5},
            'net_margin': {'excellent': 15, 'good': 8, 'average': 4, 'poor': 1},
            'operating_margin': {'excellent': 20, 'good': 12, 'average': 6, 'poor': 2},
            'roa': {'excellent': 12, 'good': 6, 'average': 3, 'poor': 1},
            'roe': {'excellent': 20, 'good': 12, 'average': 6, 'poor': 2},
            'debt_ratio': {'excellent': 20, 'good': 30, 'average': 50, 'poor': 70},
            'current_ratio': {'excellent': 2.0, 'good': 1.5, 'average': 1.2, 'poor': 1.0}
        }
        
        # 各產業專用評分標準
        self.industry_scoring = {
            "科技業": {
                'revenue_growth_rate': {'excellent': 20, 'good': 12, 'average': 5, 'poor': -10},
                'gross_margin': {'excellent': 45, 'good': 35, 'average': 25, 'poor': 15},
                'net_margin': {'excellent': 20, 'good': 15, 'average': 10, 'poor': 5},
                'operating_margin': {'excellent': 25, 'good': 18, 'average': 12, 'poor': 6},
                'roa': {'excellent': 15, 'good': 10, 'average': 6, 'poor': 3},
                'roe': {'excellent': 25, 'good': 18, 'average': 12, 'poor': 6},
                'debt_ratio': {'excellent': 25, 'good': 35, 'average': 45, 'poor': 55},
                'current_ratio': {'excellent': 2.5, 'good': 2.0, 'average': 1.5, 'poor': 1.2},
                'adjustments': {
                    '提高標準': ['毛利率', '淨利率', 'ROE', 'ROA'],
                    '降低標準': ['負債比'],
                    '特殊考量': '重視成長性與獲利能力，對週期性波動較寬容'
                }
            },
            
            "金融業": {
                'revenue_growth_rate': {'excellent': 10, 'good': 6, 'average': 3, 'poor': 0},
                'gross_margin': None,  # 不適用
                'net_margin': {'excellent': 35, 'good': 25, 'average': 15, 'poor': 10},
                'operating_margin': {'excellent': 40, 'good': 30, 'average': 20, 'poor': 12},
                'roa': {'excellent': 1.5, 'good': 1.0, 'average': 0.7, 'poor': 0.4},
                'roe': {'excellent': 15, 'good': 12, 'average': 8, 'poor': 5},
                'debt_ratio': {'excellent': 92, 'good': 89, 'average': 85, 'poor': 80},  # 反向評分
                'current_ratio': None,  # 不適用於金融業
                'nim': {'excellent': 1.8, 'good': 1.4, 'average': 1.0, 'poor': 0.7},  # 淨利差
                'adjustments': {
                    '特殊指標': ['淨利差(NIM)', '逾放比', '資本適足率'],
                    '降低標準': ['ROA', '營收成長率'],
                    '提高標準': ['負債比容忍度'],
                    '特殊考量': '高負債比為正常，重視資本效率與風險管理'
                }
            },
            
            "傳統製造業": {
                'revenue_growth_rate': {'excellent': 10, 'good': 5, 'average': 0, 'poor': -10},
                'gross_margin': {'excellent': 20, 'good': 15, 'average': 10, 'poor': 5},
                'net_margin': {'excellent': 10, 'good': 6, 'average': 3, 'poor': 1},
                'operating_margin': {'excellent': 12, 'good': 8, 'average': 4, 'poor': 1},
                'roa': {'excellent': 8, 'good': 5, 'average': 3, 'poor': 1},
                'roe': {'excellent': 12, 'good': 8, 'average': 5, 'poor': 2},
                'debt_ratio': {'excellent': 35, 'good': 45, 'average': 55, 'poor': 65},
                'current_ratio': {'excellent': 1.8, 'good': 1.4, 'average': 1.1, 'poor': 0.9},
                'adjustments': {
                    '降低標準': ['毛利率', '淨利率', 'ROE', 'ROA', '營收成長率'],
                    '提高容忍': ['負債比', '週期性波動'],
                    '特殊考量': '重視成本控制能力與現金流穩定性'
                }
            },
            
            "零售業": {
                'revenue_growth_rate': {'excellent': 12, 'good': 7, 'average': 3, 'poor': 0},
                'gross_margin': {'excellent': 35, 'good': 28, 'average': 22, 'poor': 15},
                'net_margin': {'excellent': 8, 'good': 5, 'average': 3, 'poor': 1},
                'operating_margin': {'excellent': 10, 'good': 6, 'average': 3, 'poor': 1},
                'roa': {'excellent': 15, 'good': 10, 'average': 6, 'poor': 3},
                'roe': {'excellent': 20, 'good': 15, 'average': 10, 'poor': 5},
                'debt_ratio': {'excellent': 30, 'good': 40, 'average': 50, 'poor': 60},
                'current_ratio': {'excellent': 1.5, 'good': 1.2, 'average': 1.0, 'poor': 0.8},
                'inventory_turnover': {'excellent': 12, 'good': 8, 'average': 6, 'poor': 4},
                'adjustments': {
                    '提高標準': ['資產周轉率', '存貨周轉率'],
                    '降低標準': ['淨利率'],
                    '特殊指標': ['同店成長率', '坪效'],
                    '特殊考量': '重視營運效率與現金流管理'
                }
            },
            
            "公用事業": {
                'revenue_growth_rate': {'excellent': 6, 'good': 4, 'average': 2, 'poor': 0},
                'gross_margin': {'excellent': 50, 'good': 40, 'average': 30, 'poor': 20},
                'net_margin': {'excellent': 18, 'good': 14, 'average': 10, 'poor': 6},
                'operating_margin': {'excellent': 22, 'good': 16, 'average': 12, 'poor': 8},
                'roa': {'excellent': 10, 'good': 7, 'average': 4, 'poor': 2},
                'roe': {'excellent': 15, 'good': 12, 'average': 8, 'poor': 5},
                'debt_ratio': {'excellent': 25, 'good': 35, 'average': 45, 'poor': 55},
                'current_ratio': {'excellent': 1.8, 'good': 1.4, 'average': 1.1, 'poor': 0.9},
                'adjustments': {
                    '降低標準': ['營收成長率'],
                    '提高標準': ['毛利率', '獲利穩定性'],
                    '特殊考量': '重視獲利穩定性與股息配發能力'
                }
            }
        }
    
    def get_scoring_comparison(self):
        """生成評分標準比較表"""
        comparison_data = []
        
        metrics = ['revenue_growth_rate', 'gross_margin', 'net_margin', 'roa', 'roe', 'debt_ratio']
        metric_names = ['營收成長率', '毛利率', '淨利率', 'ROA', 'ROE', '負債比']
        
        for industry, scoring in self.industry_scoring.items():
            row = {'產業': industry}
            for i, metric in enumerate(metrics):
                if scoring.get(metric) is not None:
                    excellent = scoring[metric]['excellent']
                    if metric == 'debt_ratio':  # 負債比是反向指標
                        row[metric_names[i]] = f"<{excellent}%"
                    else:
                        row[metric_names[i]] = f">{excellent}%" if metric in ['gross_margin', 'net_margin', 'roa', 'roe'] else f">{excellent}%"
                else:
                    row[metric_names[i]] = "N/A"
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def generate_adjustment_recommendations(self):
        """生成調整建議報告"""
        report = []
        report.append("📊 台灣各產業財務健康度評分標準調整建議")
        report.append("=" * 80)
        report.append("")
        
        report.append("🎯 調整原則:")
        report.append("1. 基於各產業的營運特性與財務結構差異")
        report.append("2. 參考台股市場實際表現數據")
        report.append("3. 考量產業生命週期與競爭態勢")
        report.append("4. 納入產業特有風險因子")
        report.append("")
        
        for industry, scoring in self.industry_scoring.items():
            report.append(f"🏭 {industry} 評分標準調整")
            report.append("-" * 40)
            
            # 具體評分標準
            report.append("📈 具體評分門檻 (優秀等級):")
            for metric, thresholds in scoring.items():
                if metric != 'adjustments' and thresholds is not None:
                    metric_name = {
                        'revenue_growth_rate': '營收成長率',
                        'gross_margin': '毛利率',
                        'net_margin': '淨利率',
                        'roa': 'ROA',
                        'roe': 'ROE',
                        'debt_ratio': '負債比',
                        'nim': '淨利差'
                    }.get(metric, metric)
                    
                    if metric == 'debt_ratio':
                        report.append(f"  • {metric_name}: <{thresholds['excellent']}% (越低越好)")
                    else:
                        report.append(f"  • {metric_name}: >{thresholds['excellent']}%")
            
            # 調整說明
            if 'adjustments' in scoring:
                adj = scoring['adjustments']
                report.append("")
                report.append("⚖️ 調整說明:")
                for key, value in adj.items():
                    if isinstance(value, list):
                        report.append(f"  • {key}: {', '.join(value)}")
                    else:
                        report.append(f"  • {key}: {value}")
            
            report.append("")
            report.append("-" * 60)
            report.append("")
        
        # 權重調整建議
        report.append("⚖️ 各產業權重配置調整建議")
        report.append("=" * 50)
        
        weight_recommendations = {
            "科技業": {
                "rationale": "重視創新能力與獲利表現",
                "adjustments": [
                    "盈利能力權重提升至45% (+5%)",
                    "現金流權重降至15% (-5%)",
                    "原因: 科技業週期性強，獲利能力比現金流更重要"
                ]
            },
            "金融業": {
                "rationale": "重視資本效率與風險管理",
                "adjustments": [
                    "每股指標權重提升至30% (+5%)",
                    "現金流權重降至10% (-10%)",
                    "財務結構權重提升至25% (+10%)",
                    "原因: 金融業現金流結構特殊，更重視資本運用效率"
                ]
            },
            "傳統製造業": {
                "rationale": "重視現金流穩定性與成本控制",
                "adjustments": [
                    "現金流權重提升至30% (+10%)",
                    "盈利能力權重降至35% (-5%)",
                    "每股指標權重降至20% (-5%)",
                    "原因: 週期性產業更需要關注現金流與財務穩健度"
                ]
            },
            "零售業": {
                "rationale": "重視營運效率與現金管理",
                "adjustments": [
                    "現金流權重提升至25% (+5%)",
                    "財務結構權重提升至20% (+5%)",
                    "盈利能力權重降至30% (-10%)",
                    "原因: 零售業重視周轉率與現金流管理"
                ]
            },
            "公用事業": {
                "rationale": "重視獲利穩定性與財務安全",
                "adjustments": [
                    "財務結構權重提升至25% (+10%)",
                    "盈利能力權重降至30% (-10%)",
                    "原因: 公用事業重視穩定性勝過成長性"
                ]
            }
        }
        
        for industry, rec in weight_recommendations.items():
            report.append(f"\n🏭 {industry}")
            report.append(f"   核心理念: {rec['rationale']}")
            for adj in rec['adjustments']:
                report.append(f"   • {adj}")
        
        return "\n".join(report)
    
    def get_implementation_guide(self):
        """獲取實施指引"""
        guide = []
        guide.append("🔧 評分標準調整實施指引")
        guide.append("=" * 50)
        guide.append("")
        
        guide.append("📋 實施步驟:")
        guide.append("1. 股票產業分類")
        guide.append("   - 根據上市櫃公司產業別代碼分類")
        guide.append("   - 或使用yfinance的sector/industry資訊")
        guide.append("   - 建議建立產業對照表")
        guide.append("")
        
        guide.append("2. 動態評分標準選擇")
        guide.append("   - 程式自動偵測股票產業別")
        guide.append("   - 載入對應的評分標準")
        guide.append("   - 套用產業專屬權重配置")
        guide.append("")
        
        guide.append("3. 評分計算調整")
        guide.append("   - 保持原有評分邏輯架構")
        guide.append("   - 僅調整評分門檻數值")
        guide.append("   - 權重係數動態配置")
        guide.append("")
        
        guide.append("4. 結果呈現優化")
        guide.append("   - 標註使用的產業評分標準")
        guide.append("   - 提供產業平均值比較")
        guide.append("   - 增加產業排名資訊")
        guide.append("")
        
        guide.append("💡 注意事項:")
        guide.append("• 混合營業的公司需人工判斷主要業務")
        guide.append("• 新興產業可參考最相近的傳統產業標準")
        guide.append("• 定期檢視調整標準的合理性")
        guide.append("• 保留通用標準作為備案")
        
        return "\n".join(guide)


def main():
    """主程式展示"""
    recommender = IndustryScoringRecommendations()
    
    # 生成完整建議報告
    print(recommender.generate_adjustment_recommendations())
    
    print("\n" + "="*80)
    
    # 評分標準比較表
    print("\n📊 各產業優秀等級評分門檻比較")
    print("="*60)
    comparison_df = recommender.get_scoring_comparison()
    print(comparison_df.to_string(index=False))
    
    print("\n" + "="*80)
    
    # 實施指引
    print(recommender.get_implementation_guide())


if __name__ == "__main__":
    main()