#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台灣行業別財務健康度評分系統

這個模組提供基於台灣股市特性的行業別財務健康度評分功能
支援13個主要行業的客製化評分標準和權重配置

Author: AI Assistant
Created: 2024-12-19
"""

import json
import os
from typing import Dict, Any, Optional, Tuple


class TaiwanIndustryScorer:
    """台灣行業別財務健康度評分器"""
    
    def __init__(self, json_file_path: Optional[str] = None):
        """
        初始化評分器
        
        Parameters:
        json_file_path (str, optional): JSON檔案路徑，預設為同目錄下的檔案
        """
        if json_file_path is None:
            # 預設使用同目錄下的JSON檔案
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(current_dir, 'taiwan_industry_scoring_standards.json')
        
        self.json_file_path = json_file_path
        self.standards = self._load_standards()
        
    def _load_standards(self) -> Dict[str, Any]:
        """載入評分標準JSON檔案"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到評分標準檔案: {self.json_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON檔案格式錯誤: {e}")
    
    def reload_standards(self) -> None:
        """重新載入評分標準（用於檔案更新後）"""
        self.standards = self._load_standards()
        print("✅ 評分標準已重新載入")
    
    def get_industry_mapping(self, yfinance_sector: str) -> str:
        """
        將yfinance的sector轉換為台灣行業分類
        
        Parameters:
        yfinance_sector (str): yfinance的產業分類
        
        Returns:
        str: 台灣行業分類
        """
        mapping = self.standards.get('industry_mapping', {}).get('yfinance_to_taiwan', {})
        return mapping.get(yfinance_sector, '通用')
    
    def get_industry_weights(self, taiwan_industry: str) -> Optional[Dict[str, float]]:
        """
        取得指定行業的權重配置
        
        Parameters:
        taiwan_industry (str): 台灣行業分類
        
        Returns:
        Dict[str, float]: 權重配置字典
        """
        industry_weights = self.standards.get('industry_weights', {})
        if taiwan_industry in industry_weights:
            weights = industry_weights[taiwan_industry].copy()
            # 移除描述欄位，只保留權重數值
            weights.pop('description', None)
            return weights
        return industry_weights.get('通用', {})
    
    def get_scoring_criteria(self, taiwan_industry: str) -> Optional[Dict[str, Any]]:
        """
        取得指定行業的評分標準
        
        Parameters:
        taiwan_industry (str): 台灣行業分類
        
        Returns:
        Dict[str, Any]: 評分標準字典
        """
        scoring_criteria = self.standards.get('scoring_criteria', {})
        if taiwan_industry in scoring_criteria:
            return scoring_criteria[taiwan_industry]
        return scoring_criteria.get('通用', {})
    
    def get_industry_info(self, taiwan_industry: str) -> Dict[str, Any]:
        """
        取得行業完整資訊
        
        Parameters:
        taiwan_industry (str): 台灣行業分類
        
        Returns:
        Dict[str, Any]: 包含權重、評分標準、典型公司等資訊
        """
        info = {
            'industry': taiwan_industry,
            'weights': self.get_industry_weights(taiwan_industry),
            'scoring_criteria': self.get_scoring_criteria(taiwan_industry),
            'typical_companies': self.standards.get('typical_companies', {}).get(taiwan_industry, [])
        }
        
        # 添加權重描述
        industry_weights = self.standards.get('industry_weights', {})
        if taiwan_industry in industry_weights:
            info['description'] = industry_weights[taiwan_industry].get('description', '')
        
        return info
    
    def score_metric(self, value: float, metric_name: str, taiwan_industry: str) -> Tuple[int, str]:
        """
        對單一指標進行評分
        
        Parameters:
        value (float): 指標數值
        metric_name (str): 指標名稱
        taiwan_industry (str): 台灣行業分類
        
        Returns:
        Tuple[int, str]: (分數, 等級)
        """
        criteria = self.get_scoring_criteria(taiwan_industry)
        
        if not criteria or metric_name not in criteria:
            return 0, 'N/A'
        
        metric_criteria = criteria[metric_name]
        reverse = metric_criteria.get('reverse', False)
        
        if value is None:
            return 0, 'N/A'
        
        if not reverse:
            # 數值越高越好
            if value >= metric_criteria['excellent']:
                return 100, 'Excellent'
            elif value >= metric_criteria['good']:
                return 80, 'Good'
            elif value >= metric_criteria['average']:
                return 60, 'Average'
            elif value >= metric_criteria['poor']:
                return 40, 'Poor'
            else:
                return 20, 'Very Poor'
        else:
            # 數值越低越好（如負債比）
            if value <= metric_criteria['excellent']:
                return 100, 'Excellent'
            elif value <= metric_criteria['good']:
                return 80, 'Good'
            elif value <= metric_criteria['average']:
                return 60, 'Average'
            elif value <= metric_criteria['poor']:
                return 40, 'Poor'
            else:
                return 20, 'Very Poor'
    
    def calculate_industry_score(self, metrics: Dict[str, float], yfinance_sector: str) -> Dict[str, Any]:
        """
        計算行業別財務健康度總分
        
        Parameters:
        metrics (Dict[str, float]): 財務指標字典
        yfinance_sector (str): yfinance產業分類
        
        Returns:
        Dict[str, Any]: 包含各項評分和總分的字典
        """
        # 轉換為台灣行業分類
        taiwan_industry = self.get_industry_mapping(yfinance_sector)
        
        # 取得權重和評分標準
        weights = self.get_industry_weights(taiwan_industry)
        criteria = self.get_scoring_criteria(taiwan_industry)
        
        if not weights or not criteria:
            raise ValueError(f"找不到行業 '{taiwan_industry}' 的評分標準")
        
        scores = {}
        
        # 計算各項指標評分
        profitability_scores = []
        per_share_scores = []
        cashflow_scores = []
        financial_structure_scores = []
        
        # 盈利能力指標
        profitability_metrics = ['revenue_growth_rate', 'gross_margin', 'net_margin', 'operating_margin', 'roa', 'roe']
        for metric in profitability_metrics:
            if metric in metrics and metric in criteria:
                score, grade = self.score_metric(metrics[metric], metric, taiwan_industry)
                scores[f'{metric}_score'] = score
                scores[f'{metric}_grade'] = grade
                profitability_scores.append(score)
        
        # 每股指標
        per_share_metrics = ['eps_growth']
        for metric in per_share_metrics:
            if metric in metrics and metric in criteria:
                score, grade = self.score_metric(metrics[metric], metric, taiwan_industry)
                scores[f'{metric}_score'] = score
                scores[f'{metric}_grade'] = grade
                per_share_scores.append(score)
        
        # EPS絕對值簡化評分
        if 'eps' in metrics and metrics['eps'] is not None:
            eps_score = min(100, max(0, metrics['eps'] * 20))
            scores['eps_score'] = eps_score
            per_share_scores.append(eps_score)
        
        # 現金流指標
        cashflow_metrics = ['ocf_to_net_income']
        for metric in cashflow_metrics:
            if metric in metrics and metric in criteria:
                score, grade = self.score_metric(metrics[metric], metric, taiwan_industry)
                scores[f'{metric}_score'] = score
                scores[f'{metric}_grade'] = grade
                cashflow_scores.append(score)
        
        # 財務結構指標
        financial_structure_metrics = ['debt_ratio', 'current_ratio']
        for metric in financial_structure_metrics:
            if metric in metrics and metric in criteria:
                score, grade = self.score_metric(metrics[metric], metric, taiwan_industry)
                scores[f'{metric}_score'] = score
                scores[f'{metric}_grade'] = grade
                financial_structure_scores.append(score)
        
        # 計算各維度平均分數
        scores['profitability_score'] = sum(profitability_scores) / len(profitability_scores) if profitability_scores else 0
        scores['per_share_score'] = sum(per_share_scores) / len(per_share_scores) if per_share_scores else 0
        scores['cashflow_score'] = sum(cashflow_scores) / len(cashflow_scores) if cashflow_scores else 50
        scores['financial_structure_score'] = sum(financial_structure_scores) / len(financial_structure_scores) if financial_structure_scores else 50
        
        # 計算加權總分
        total_score = (
            scores['profitability_score'] * weights.get('profitability', 0.4) +
            scores['per_share_score'] * weights.get('per_share', 0.25) +
            scores['cashflow_score'] * weights.get('cash_flow', 0.2) +
            scores['financial_structure_score'] * weights.get('financial_structure', 0.15)
        )
        
        scores['total_score'] = total_score
        
        # 健康度等級
        if total_score >= 80:
            scores['health_grade'] = '優秀 (Excellent)'
        elif total_score >= 60:
            scores['health_grade'] = '良好 (Good)'
        elif total_score >= 40:
            scores['health_grade'] = '普通 (Average)'
        else:
            scores['health_grade'] = '警示 (Warning)'
        
        # 添加行業資訊
        scores['taiwan_industry'] = taiwan_industry
        scores['yfinance_sector'] = yfinance_sector
        scores['weights_used'] = weights
        scores['industry_description'] = self.get_industry_info(taiwan_industry).get('description', '')
        
        return scores
    
    def get_supported_industries(self) -> list:
        """取得支援的台灣行業列表"""
        return self.standards.get('industry_mapping', {}).get('taiwan_sectors', [])
    
    def get_typical_companies(self, taiwan_industry: str) -> list:
        """取得行業典型公司列表"""
        return self.standards.get('typical_companies', {}).get(taiwan_industry, [])
    
    def print_industry_summary(self) -> None:
        """印出支援的行業摘要"""
        print("🏭 台灣行業財務健康度評分系統")
        print("=" * 60)
        
        industries = self.get_supported_industries()
        print(f"📊 支援行業數量: {len(industries)}")
        print("📋 支援的行業:")
        
        for i, industry in enumerate(industries, 1):
            typical_companies = self.get_typical_companies(industry)
            companies_str = ", ".join([f"{c['name']}({c['code'].replace('.TW', '')})" 
                                     for c in typical_companies[:3]])
            print(f"  {i:2d}. {industry:8s} - {companies_str}")
        
        print(f"\n💡 使用方法:")
        print(f"  scorer = TaiwanIndustryScorer()")
        print(f"  scores = scorer.calculate_industry_score(metrics, yfinance_sector)")


def main():
    """示範用法"""
    try:
        # 初始化評分器
        scorer = TaiwanIndustryScorer()
        
        # 顯示支援的行業
        scorer.print_industry_summary()
        
        # 示範取得行業資訊
        print(f"\n🔍 科技業評分標準範例:")
        tech_info = scorer.get_industry_info('科技業')
        print(f"  權重配置: {tech_info['weights']}")
        print(f"  產業描述: {tech_info['description']}")
        
        # 示範指標評分
        print(f"\n📊 指標評分範例:")
        score, grade = scorer.score_metric(55, 'gross_margin', '科技業')
        print(f"  科技業毛利率 55% 評分: {score}分 ({grade})")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")


if __name__ == "__main__":
    main()