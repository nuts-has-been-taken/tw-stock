#!/usr/bin/env python3
"""
簡化版ETF測試程式
用於驗證ETF數據收集邏輯
"""

import json
import os
from datetime import datetime

def create_test_etf_data():
    """創建測試用的ETF數據"""
    
    # 測試用ETF清單
    etf_list = [
        {'code': '0050', 'name': '元大台灣50', 'full_code': '0050.TW', 'type': '股票型ETF'},
        {'code': '0056', 'name': '元大高股息', 'full_code': '0056.TW', 'type': '股票型ETF'},
        {'code': '00878', 'name': '國泰永續高股息', 'full_code': '00878.TW', 'type': '股票型ETF'},
        {'code': '00881', 'name': '國泰台灣5G+', 'full_code': '00881.TW', 'type': '股票型ETF'},
        {'code': '00692', 'name': '富邦公司治理', 'full_code': '00692.TW', 'type': '股票型ETF'}
    ]
    
    # 測試用成份股數據
    etf_constituents = {
        '0050': {
            'name': '元大台灣50',
            'type': '股票型ETF',
            'constituents': [
                {'stock_code': '2330', 'stock_name': '台積電', 'weight': 47.52},
                {'stock_code': '2454', 'stock_name': '聯發科', 'weight': 8.23},
                {'stock_code': '2317', 'stock_name': '鴻海', 'weight': 4.15},
                {'stock_code': '2308', 'stock_name': '台達電', 'weight': 2.87},
                {'stock_code': '2881', 'stock_name': '富邦金', 'weight': 2.53}
            ],
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        '0056': {
            'name': '元大高股息',
            'type': '股票型ETF',
            'constituents': [
                {'stock_code': '2330', 'stock_name': '台積電', 'weight': 15.23},
                {'stock_code': '2454', 'stock_name': '聯發科', 'weight': 8.91},
                {'stock_code': '2317', 'stock_name': '鴻海', 'weight': 6.72},
                {'stock_code': '2891', 'stock_name': '中信金', 'weight': 4.33},
                {'stock_code': '2881', 'stock_name': '富邦金', 'weight': 3.84}
            ],
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        '00878': {
            'name': '國泰永續高股息',
            'type': '股票型ETF',
            'constituents': [
                {'stock_code': '2330', 'stock_name': '台積電', 'weight': 12.45},
                {'stock_code': '2454', 'stock_name': '聯發科', 'weight': 7.86},
                {'stock_code': '2317', 'stock_name': '鴻海', 'weight': 6.23},
                {'stock_code': '2891', 'stock_name': '中信金', 'weight': 5.12},
                {'stock_code': '2881', 'stock_name': '富邦金', 'weight': 4.78}
            ],
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    
    return etf_list, etf_constituents

def analyze_etf_overlap(etf1_constituents, etf2_constituents):
    """分析兩個ETF的重疊度"""
    etf1_stocks = {stock['stock_code'] for stock in etf1_constituents}
    etf2_stocks = {stock['stock_code'] for stock in etf2_constituents}
    
    overlap_stocks = etf1_stocks & etf2_stocks
    total_unique = etf1_stocks | etf2_stocks
    
    overlap_ratio = len(overlap_stocks) / len(total_unique) if total_unique else 0
    
    return {
        'overlap_stocks': list(overlap_stocks),
        'overlap_count': len(overlap_stocks),
        'overlap_ratio': overlap_ratio,
        'total_unique': len(total_unique)
    }

def calculate_stock_frequency(etf_constituents):
    """計算股票在各ETF中出現的頻率"""
    stock_frequency = {}
    stock_total_weight = {}
    
    for etf_code, data in etf_constituents.items():
        for constituent in data['constituents']:
            stock_code = constituent['stock_code']
            stock_name = constituent['stock_name']
            weight = constituent['weight']
            
            if stock_code not in stock_frequency:
                stock_frequency[stock_code] = {
                    'name': stock_name,
                    'count': 0,
                    'total_weight': 0,
                    'etfs': []
                }
            
            stock_frequency[stock_code]['count'] += 1
            stock_frequency[stock_code]['total_weight'] += weight
            stock_frequency[stock_code]['etfs'].append({
                'etf_code': etf_code,
                'etf_name': data['name'],
                'weight': weight
            })
    
    return stock_frequency

def save_analysis_results(etf_list, etf_constituents, data_dir="../data/etf_data/"):
    """儲存分析結果"""
    os.makedirs(data_dir, exist_ok=True)
    
    # 儲存ETF清單
    with open(os.path.join(data_dir, 'etf_list.json'), 'w', encoding='utf-8') as f:
        json.dump(etf_list, f, ensure_ascii=False, indent=2)
    
    # 儲存成份股資料
    with open(os.path.join(data_dir, 'etf_constituents.json'), 'w', encoding='utf-8') as f:
        json.dump(etf_constituents, f, ensure_ascii=False, indent=2)
    
    # 創建CSV格式的摘要
    csv_content = "ETF代碼,ETF名稱,股票代碼,股票名稱,權重,更新時間\n"
    
    for etf_code, data in etf_constituents.items():
        for constituent in data['constituents']:
            csv_content += f"{etf_code},{data['name']},{constituent['stock_code']},{constituent['stock_name']},{constituent['weight']},{data['last_update']}\n"
    
    with open(os.path.join(data_dir, 'all_etf_constituents.csv'), 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    print(f"分析結果已儲存至: {data_dir}")

def print_analysis_report(etf_list, etf_constituents):
    """列印分析報告"""
    print("=" * 60)
    print("台股ETF成份股分析測試報告")
    print("=" * 60)
    
    print(f"\n📊 基本統計:")
    print(f"  - 分析ETF數量: {len(etf_constituents)}")
    
    total_records = sum(len(data['constituents']) for data in etf_constituents.values())
    print(f"  - 總成份股記錄: {total_records}")
    
    # 計算股票頻率
    stock_freq = calculate_stock_frequency(etf_constituents)
    unique_stocks = len(stock_freq)
    print(f"  - 獨特股票數量: {unique_stocks}")
    
    print(f"\n🏆 最常出現的股票:")
    sorted_stocks = sorted(stock_freq.items(), key=lambda x: x[1]['count'], reverse=True)
    for i, (stock_code, info) in enumerate(sorted_stocks[:5], 1):
        print(f"  {i}. {stock_code} {info['name']}: 出現在 {info['count']} 檔ETF中")
    
    print(f"\n💰 總權重最高的股票:")
    sorted_by_weight = sorted(stock_freq.items(), key=lambda x: x[1]['total_weight'], reverse=True)
    for i, (stock_code, info) in enumerate(sorted_by_weight[:5], 1):
        print(f"  {i}. {stock_code} {info['name']}: 總權重 {info['total_weight']:.2f}%")
    
    print(f"\n🔍 ETF重疊度分析:")
    if '0050' in etf_constituents and '0056' in etf_constituents:
        overlap = analyze_etf_overlap(
            etf_constituents['0050']['constituents'],
            etf_constituents['0056']['constituents']
        )
        print(f"  - 0050 與 0056 重疊:")
        print(f"    重疊股票數: {overlap['overlap_count']}")
        print(f"    重疊比例: {overlap['overlap_ratio']:.2%}")
        print(f"    重疊股票: {', '.join(overlap['overlap_stocks'])}")
    
    print(f"\n📈 個別ETF分析:")
    for etf_code, data in etf_constituents.items():
        print(f"\n  {etf_code} - {data['name']}:")
        print(f"    成份股數量: {len(data['constituents'])}")
        print(f"    前三大持股:")
        for i, constituent in enumerate(data['constituents'][:3], 1):
            print(f"      {i}. {constituent['stock_code']} {constituent['stock_name']}: {constituent['weight']}%")
    
    print("\n" + "=" * 60)

def main():
    """主程式"""
    print("台股ETF成份股分析測試程式")
    print("=" * 40)
    
    # 創建測試數據
    etf_list, etf_constituents = create_test_etf_data()
    
    # 執行分析
    print_analysis_report(etf_list, etf_constituents)
    
    # 儲存結果
    save_analysis_results(etf_list, etf_constituents)
    
    print(f"\n✅ 測試程式執行完成！")
    
    # 驗證儲存的檔案
    data_dir = "../data/etf_data/"
    files_created = []
    for filename in ['etf_list.json', 'etf_constituents.json', 'all_etf_constituents.csv']:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            files_created.append(filename)
    
    print(f"已創建檔案: {', '.join(files_created)}")

if __name__ == "__main__":
    main()