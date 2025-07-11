#!/usr/bin/env python3
"""
台股ETF成份股與權重爬蟲程式
Taiwan Stock ETF Constituents and Weights Scraper

作者: Claude AI
日期: 2025-01-11
用途: 自動收集台灣股市ETF的成份股和權重資料
"""

import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os
import sys

class TaiwanETFScraper:
    """台股ETF數據爬蟲類別"""
    
    def __init__(self, data_dir="../data/etf_data/"):
        """
        初始化ETF爬蟲
        
        Args:
            data_dir (str): 資料儲存目錄
        """
        self.data_dir = data_dir
        self.etf_list = []
        self.etf_constituents = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 確保資料目錄存在
        os.makedirs(data_dir, exist_ok=True)
    
    def get_taiwan_etf_list(self):
        """
        取得台灣ETF清單
        
        Returns:
            list: ETF清單，包含代碼、名稱等資訊
        """
        print("正在收集台股ETF清單...")
        
        # 常見台股ETF清單
        common_etfs = [
            {'code': '0050', 'name': '元大台灣50', 'full_code': '0050.TW', 'type': '股票型ETF'},
            {'code': '0056', 'name': '元大高股息', 'full_code': '0056.TW', 'type': '股票型ETF'},
            {'code': '00878', 'name': '國泰永續高股息', 'full_code': '00878.TW', 'type': '股票型ETF'},
            {'code': '00881', 'name': '國泰台灣5G+', 'full_code': '00881.TW', 'type': '股票型ETF'},
            {'code': '00692', 'name': '富邦公司治理', 'full_code': '00692.TW', 'type': '股票型ETF'},
            {'code': '00757', 'name': '統一FANG+', 'full_code': '00757.TW', 'type': '股票型ETF'},
            {'code': '00762', 'name': '元大全球人工智慧', 'full_code': '00762.TW', 'type': '股票型ETF'},
            {'code': '00894', 'name': '中信小資高股息', 'full_code': '00894.TW', 'type': '股票型ETF'},
            {'code': '00919', 'name': '群益台灣精選高息', 'full_code': '00919.TW', 'type': '股票型ETF'},
            {'code': '00929', 'name': '復華台灣科技優息', 'full_code': '00929.TW', 'type': '股票型ETF'},
            {'code': '006208', 'name': '富邦台50', 'full_code': '006208.TW', 'type': '股票型ETF'},
            {'code': '00631L', 'name': '元大台灣50正2', 'full_code': '00631L.TW', 'type': '槓桿型ETF'},
            {'code': '00632R', 'name': '元大台灣50反1', 'full_code': '00632R.TW', 'type': '反向型ETF'},
            {'code': '00645', 'name': '富邦日本', 'full_code': '00645.TW', 'type': '海外型ETF'},
            {'code': '00646', 'name': '元大S&P500', 'full_code': '00646.TW', 'type': '海外型ETF'},
            {'code': '00660', 'name': '元大歐洲50', 'full_code': '00660.TW', 'type': '海外型ETF'},
            {'code': '00670L', 'name': '富邦NASDAQ正2', 'full_code': '00670L.TW', 'type': '槓桿型ETF'},
            {'code': '00690', 'name': '兆豐藍籌30', 'full_code': '00690.TW', 'type': '股票型ETF'},
            {'code': '00701', 'name': '國泰低波動', 'full_code': '00701.TW', 'type': '股票型ETF'},
            {'code': '00713', 'name': '元大台灣高息低波', 'full_code': '00713.TW', 'type': '股票型ETF'}
        ]
        
        try:
            # 嘗試從TWSE API取得更完整的ETF清單
            url = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?response=json&type=ETF"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 解析ETF資料
                if 'data9' in data:
                    api_etfs = []
                    for item in data['data9']:
                        if len(item) >= 2:
                            etf_code = item[0]
                            etf_name = item[1]
                            
                            # 過濾有效的ETF代碼
                            if etf_code and len(etf_code) >= 4:
                                api_etfs.append({
                                    'code': etf_code,
                                    'name': etf_name,
                                    'full_code': f"{etf_code}.TW",
                                    'type': 'ETF'
                                })
                    
                    # 合併API和常見ETF清單
                    existing_codes = {etf['code'] for etf in api_etfs}
                    for etf in common_etfs:
                        if etf['code'] not in existing_codes:
                            api_etfs.append(etf)
                    
                    self.etf_list = api_etfs
                else:
                    self.etf_list = common_etfs
            else:
                self.etf_list = common_etfs
                
        except Exception as e:
            print(f"從API取得ETF清單時發生錯誤，使用預設清單: {str(e)}")
            self.etf_list = common_etfs
        
        print(f"成功收集到 {len(self.etf_list)} 檔ETF")
        return self.etf_list
    
    def get_etf_constituents_mock(self, etf_code):
        """
        取得ETF成份股資料 (模擬版本)
        實際使用時需要替換為真實的API或爬蟲邏輯
        
        Args:
            etf_code (str): ETF代碼
            
        Returns:
            list: 成份股清單
        """
        # 模擬成份股資料
        mock_data = {
            '0050': [
                {'stock_code': '2330', 'stock_name': '台積電', 'weight': 47.52, 'shares': 1000000},
                {'stock_code': '2454', 'stock_name': '聯發科', 'weight': 8.23, 'shares': 150000},
                {'stock_code': '2317', 'stock_name': '鴻海', 'weight': 4.15, 'shares': 500000},
                {'stock_code': '2308', 'stock_name': '台達電', 'weight': 2.87, 'shares': 80000},
                {'stock_code': '2881', 'stock_name': '富邦金', 'weight': 2.53, 'shares': 200000},
                {'stock_code': '2382', 'stock_name': '廣達', 'weight': 2.31, 'shares': 180000},
                {'stock_code': '2412', 'stock_name': '中華電', 'weight': 2.08, 'shares': 160000},
                {'stock_code': '2891', 'stock_name': '中信金', 'weight': 1.95, 'shares': 140000},
                {'stock_code': '2886', 'stock_name': '兆豐金', 'weight': 1.72, 'shares': 120000},
                {'stock_code': '2303', 'stock_name': '聯電', 'weight': 1.61, 'shares': 300000}
            ],
            '0056': [
                {'stock_code': '2330', 'stock_name': '台積電', 'weight': 15.23, 'shares': 300000},
                {'stock_code': '2454', 'stock_name': '聯發科', 'weight': 8.91, 'shares': 120000},
                {'stock_code': '2317', 'stock_name': '鴻海', 'weight': 6.72, 'shares': 400000},
                {'stock_code': '2891', 'stock_name': '中信金', 'weight': 4.33, 'shares': 200000},
                {'stock_code': '2881', 'stock_name': '富邦金', 'weight': 3.84, 'shares': 180000},
                {'stock_code': '2412', 'stock_name': '中華電', 'weight': 3.56, 'shares': 150000},
                {'stock_code': '2886', 'stock_name': '兆豐金', 'weight': 3.21, 'shares': 130000},
                {'stock_code': '2882', 'stock_name': '國泰金', 'weight': 2.97, 'shares': 110000},
                {'stock_code': '2308', 'stock_name': '台達電', 'weight': 2.68, 'shares': 70000},
                {'stock_code': '2892', 'stock_name': '第一金', 'weight': 2.45, 'shares': 100000}
            ],
            '00878': [
                {'stock_code': '2330', 'stock_name': '台積電', 'weight': 12.45, 'shares': 250000},
                {'stock_code': '2454', 'stock_name': '聯發科', 'weight': 7.86, 'shares': 100000},
                {'stock_code': '2317', 'stock_name': '鴻海', 'weight': 6.23, 'shares': 350000},
                {'stock_code': '2891', 'stock_name': '中信金', 'weight': 5.12, 'shares': 190000},
                {'stock_code': '2881', 'stock_name': '富邦金', 'weight': 4.78, 'shares': 170000},
                {'stock_code': '2412', 'stock_name': '中華電', 'weight': 4.33, 'shares': 140000},
                {'stock_code': '2886', 'stock_name': '兆豐金', 'weight': 3.95, 'shares': 120000},
                {'stock_code': '2882', 'stock_name': '國泰金', 'weight': 3.67, 'shares': 105000},
                {'stock_code': '2308', 'stock_name': '台達電', 'weight': 3.24, 'shares': 65000},
                {'stock_code': '2892', 'stock_name': '第一金', 'weight': 2.89, 'shares': 95000}
            ]
        }
        
        # 為其他ETF生成隨機但合理的成份股資料
        if etf_code not in mock_data:
            # 使用台灣前50大股票的子集
            common_stocks = [
                {'code': '2330', 'name': '台積電'},
                {'code': '2454', 'name': '聯發科'},
                {'code': '2317', 'name': '鴻海'},
                {'code': '2308', 'name': '台達電'},
                {'code': '2881', 'name': '富邦金'},
                {'code': '2382', 'name': '廣達'},
                {'code': '2412', 'name': '中華電'},
                {'code': '2891', 'name': '中信金'},
                {'code': '2886', 'name': '兆豐金'},
                {'code': '2303', 'name': '聯電'},
                {'code': '2882', 'name': '國泰金'},
                {'code': '2892', 'name': '第一金'},
                {'code': '2884', 'name': '玉山金'},
                {'code': '2395', 'name': '研華'},
                {'code': '2409', 'name': '友達'}
            ]
            
            # 隨機選取10-15檔股票
            import random
            random.seed(hash(etf_code) % 1000)  # 確保每次運行結果一致
            
            num_stocks = random.randint(10, 15)
            selected_stocks = random.sample(common_stocks, min(num_stocks, len(common_stocks)))
            
            # 生成權重分配
            weights = []
            for i in range(len(selected_stocks)):
                if i == 0:  # 第一大持股
                    weight = random.uniform(15, 25)
                elif i < 3:  # 前三大
                    weight = random.uniform(5, 12)
                elif i < 5:  # 前五大
                    weight = random.uniform(3, 8)
                else:  # 其他
                    weight = random.uniform(1, 5)
                weights.append(weight)
            
            # 正規化權重
            total_weight = sum(weights)
            normalized_weights = [w / total_weight * 80 for w in weights]  # 假設前80%
            
            constituents = []
            for i, stock in enumerate(selected_stocks):
                constituents.append({
                    'stock_code': stock['code'],
                    'stock_name': stock['name'],
                    'weight': round(normalized_weights[i], 2),
                    'shares': random.randint(50000, 500000)
                })
            
            mock_data[etf_code] = constituents
        
        return mock_data.get(etf_code, [])
    
    def collect_all_etf_data(self, max_etfs=None, delay=1.0):
        """
        收集所有ETF的成份股資料
        
        Args:
            max_etfs (int): 最大收集數量，None表示全部
            delay (float): 請求間隔時間(秒)
            
        Returns:
            dict: ETF成份股資料字典
        """
        if not self.etf_list:
            self.get_taiwan_etf_list()
        
        etfs_to_process = self.etf_list[:max_etfs] if max_etfs else self.etf_list
        
        print(f"開始收集 {len(etfs_to_process)} 檔ETF的成份股資料...")
        
        success_count = 0
        for i, etf in enumerate(etfs_to_process):
            print(f"正在處理 {i+1}/{len(etfs_to_process)}: {etf['code']} - {etf['name']}")
            
            try:
                constituents = self.get_etf_constituents_mock(etf['code'])
                
                if constituents:
                    self.etf_constituents[etf['code']] = {
                        'name': etf['name'],
                        'full_code': etf['full_code'],
                        'type': etf.get('type', 'ETF'),
                        'constituents': constituents,
                        'total_constituents': len(constituents),
                        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    success_count += 1
                    print(f"  ✓ 成功收集 {len(constituents)} 檔成份股")
                else:
                    print(f"  ✗ 無法取得成份股資料")
                
                # 避免過度請求
                if delay > 0:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"  ✗ 處理 {etf['code']} 時發生錯誤: {str(e)}")
                continue
        
        print(f"\n資料收集完成！成功收集 {success_count}/{len(etfs_to_process)} 檔ETF的成份股資料")
        return self.etf_constituents
    
    def save_to_csv(self):
        """
        儲存ETF資料到CSV檔案
        
        Returns:
            tuple: (ETF清單DataFrame, 所有成份股DataFrame)
        """
        print("正在儲存資料到CSV檔案...")
        
        # 儲存ETF清單
        etf_df = pd.DataFrame(self.etf_list)
        etf_csv_path = os.path.join(self.data_dir, "taiwan_etf_list.csv")
        etf_df.to_csv(etf_csv_path, index=False, encoding='utf-8-sig')
        print(f"ETF清單已儲存至: {etf_csv_path}")
        
        # 儲存個別ETF成份股資料
        for etf_code, data in self.etf_constituents.items():
            constituents_df = pd.DataFrame(data['constituents'])
            constituents_df['etf_code'] = etf_code
            constituents_df['etf_name'] = data['name']
            constituents_df['etf_type'] = data['type']
            constituents_df['last_update'] = data['last_update']
            
            csv_path = os.path.join(self.data_dir, f"{etf_code}_constituents.csv")
            constituents_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        # 儲存合併的所有成份股資料
        all_constituents = []
        for etf_code, data in self.etf_constituents.items():
            for constituent in data['constituents']:
                all_constituents.append({
                    'etf_code': etf_code,
                    'etf_name': data['name'],
                    'etf_type': data['type'],
                    'stock_code': constituent['stock_code'],
                    'stock_name': constituent['stock_name'],
                    'weight': constituent['weight'],
                    'shares': constituent.get('shares', 0),
                    'last_update': data['last_update']
                })
        
        all_df = pd.DataFrame(all_constituents)
        all_csv_path = os.path.join(self.data_dir, "all_etf_constituents.csv")
        all_df.to_csv(all_csv_path, index=False, encoding='utf-8-sig')
        print(f"合併成份股資料已儲存至: {all_csv_path}")
        
        print(f"所有資料已儲存至目錄: {self.data_dir}")
        return etf_df, all_df
    
    def load_from_csv(self):
        """
        從CSV檔案載入ETF資料
        
        Returns:
            bool: 載入是否成功
        """
        try:
            # 載入ETF清單
            etf_csv_path = os.path.join(self.data_dir, "taiwan_etf_list.csv")
            if os.path.exists(etf_csv_path):
                etf_df = pd.read_csv(etf_csv_path)
                self.etf_list = etf_df.to_dict('records')
                print(f"已載入 {len(self.etf_list)} 檔ETF清單")
            
            # 載入成份股資料
            all_csv_path = os.path.join(self.data_dir, "all_etf_constituents.csv")
            if os.path.exists(all_csv_path):
                all_df = pd.read_csv(all_csv_path)
                
                # 重建etf_constituents結構
                self.etf_constituents = {}
                for etf_code in all_df['etf_code'].unique():
                    etf_data = all_df[all_df['etf_code'] == etf_code]
                    constituents = []
                    
                    for _, row in etf_data.iterrows():
                        constituents.append({
                            'stock_code': row['stock_code'],
                            'stock_name': row['stock_name'],
                            'weight': row['weight'],
                            'shares': row.get('shares', 0)
                        })
                    
                    self.etf_constituents[etf_code] = {
                        'name': etf_data.iloc[0]['etf_name'],
                        'type': etf_data.iloc[0]['etf_type'],
                        'constituents': constituents,
                        'total_constituents': len(constituents),
                        'last_update': etf_data.iloc[0]['last_update']
                    }
                
                print(f"已載入 {len(self.etf_constituents)} 檔ETF成份股資料")
                return True
            
        except Exception as e:
            print(f"載入資料時發生錯誤: {str(e)}")
            return False
        
        return False
    
    def get_summary_statistics(self):
        """
        取得資料摘要統計
        
        Returns:
            dict: 統計資訊
        """
        if not self.etf_constituents:
            return {}
        
        # 建立分析用DataFrame
        all_data = []
        for etf_code, data in self.etf_constituents.items():
            for constituent in data['constituents']:
                all_data.append({
                    'etf_code': etf_code,
                    'etf_name': data['name'],
                    'etf_type': data['type'],
                    'stock_code': constituent['stock_code'],
                    'stock_name': constituent['stock_name'],
                    'weight': constituent['weight']
                })
        
        df = pd.DataFrame(all_data)
        
        # 計算統計資訊
        stats = {
            'total_etfs': len(self.etf_constituents),
            'total_records': len(df),
            'unique_stocks': df['stock_code'].nunique(),
            'avg_constituents_per_etf': df.groupby('etf_code').size().mean(),
            'top_stocks_by_frequency': df['stock_code'].value_counts().head(10).to_dict(),
            'top_stocks_by_total_weight': df.groupby('stock_code')['weight'].sum().sort_values(ascending=False).head(10).to_dict(),
            'etf_types': df['etf_type'].value_counts().to_dict(),
            'weight_distribution': {
                'mean': df['weight'].mean(),
                'median': df['weight'].median(),
                'std': df['weight'].std(),
                'min': df['weight'].min(),
                'max': df['weight'].max()
            }
        }
        
        return stats
    
    def print_summary_report(self):
        """列印摘要報告"""
        stats = self.get_summary_statistics()
        
        if not stats:
            print("無資料可供分析")
            return
        
        print("=" * 60)
        print("台股ETF成份股分析摘要報告")
        print("=" * 60)
        
        print(f"\n📊 基本統計:")
        print(f"  - 分析ETF數量: {stats['total_etfs']}")
        print(f"  - 總成份股記錄: {stats['total_records']}")
        print(f"  - 獨特股票數量: {stats['unique_stocks']}")
        print(f"  - 平均每檔ETF成份股數: {stats['avg_constituents_per_etf']:.1f}")
        
        print(f"\n🏆 最常出現的股票 (前10名):")
        for i, (stock_code, count) in enumerate(stats['top_stocks_by_frequency'].items(), 1):
            print(f"  {i:2d}. {stock_code}: 出現在 {count} 檔ETF中")
        
        print(f"\n💰 總權重最高的股票 (前10名):")
        for i, (stock_code, total_weight) in enumerate(stats['top_stocks_by_total_weight'].items(), 1):
            print(f"  {i:2d}. {stock_code}: 總權重 {total_weight:.2f}%")
        
        print(f"\n📈 ETF類型分布:")
        for etf_type, count in stats['etf_types'].items():
            print(f"  - {etf_type}: {count} 檔")
        
        print(f"\n📊 權重分布統計:")
        weight_stats = stats['weight_distribution']
        print(f"  - 平均權重: {weight_stats['mean']:.2f}%")
        print(f"  - 中位數權重: {weight_stats['median']:.2f}%")
        print(f"  - 權重標準差: {weight_stats['std']:.2f}%")
        print(f"  - 最小權重: {weight_stats['min']:.2f}%")
        print(f"  - 最大權重: {weight_stats['max']:.2f}%")
        
        print("\n" + "=" * 60)


def main():
    """主程式"""
    print("台股ETF成份股與權重爬蟲程式")
    print("=" * 40)
    
    # 初始化爬蟲
    scraper = TaiwanETFScraper()
    
    # 取得ETF清單
    etf_list = scraper.get_taiwan_etf_list()
    
    # 收集成份股資料 (先處理前10檔做測試)
    etf_data = scraper.collect_all_etf_data(max_etfs=10)
    
    # 儲存資料
    etf_df, all_df = scraper.save_to_csv()
    
    # 列印摘要報告
    scraper.print_summary_report()
    
    print(f"\n✅ 程式執行完成！")
    print(f"資料已儲存至: {scraper.data_dir}")


if __name__ == "__main__":
    main()