# Company Health Analysis Package
# 公司財務健康度分析套件

from .industry_financial_analysis import IndustryFinancialAnalyzer
from .industry_scoring_recommendations import IndustryScoringRecommendations

__version__ = "1.0.0"
__author__ = "Claude Code"
__description__ = "台灣股市公司財務健康度分析工具"

__all__ = [
    'IndustryFinancialAnalyzer',
    'IndustryScoringRecommendations'
]