from matplotlib.ticker import FuncFormatter
from datetime import datetime, timedelta
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import json
import os

def send_line_notify(msg:str, token:str, img=None):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": msg}
    if img:
        files = {'imageFile': open(img, 'rb')}
        r = requests.post(url, headers=headers, params=payload, files=files)
        return
    r = requests.post(url, headers=headers, params=payload)
    return

def get_margin(date:datetime):
    
    url = f"https://www.twse.com.tw/rwd/zh/marginTrading/MI_MARGN?date={date.strftime('%Y%m%d')}&selectType=MS&response=json&_=1724655679565"

    r = requests.get(url)
    r = json.loads(r.content)
    if r['stat'] != "OK":
        return None
    data = r['tables'][0]['data']
    res = {
        '日期':date,
        '融券(張)':eval(data[1][5].replace(',', '')),
        '融資金額(億)':float(eval(data[2][5].replace(',', ''))/100000),
    }
    
    return res

def create_margin_jpg(df:pd.DataFrame, file_path='plot.png'):
    
    # 調整字形
    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    # 處理表格
    df.set_index('日期', inplace=True)
    df = df.sort_index()
    dates = df.index
    
    # 畫圖
    def format_func(value, tick_number):
        if value == 0:
            return int(value)
        return f'{int(value)} (億)'

    fig, ax1 = plt.subplots(figsize=(10, 6))

    bar_width = 0.5
    index = np.arange(len(dates))

    margin = df['融資金額(億)']

    ax1.bar(index, margin, bar_width, label='融資金額', color='#98F5F9')
    ax1.plot(index, margin, bar_width, label='融資金額', color='#060270')

    ax1.axhline(0, color='black', linewidth=0.8, linestyle='-')
    ax1.grid(axis='y', linestyle='--', linewidth=0.7)
    ax1.set_xticks(index[::int(len(dates)/6)])
    ax1.set_xticklabels(dates[::int(len(dates)/6)].strftime('%Y-%m-%d'))
    ax1.set_xlabel('日期', rotation=0, labelpad=12)
    
    ax1.yaxis.set_major_formatter(FuncFormatter(format_func))

    plt.title('融資金額')
    plt.savefig(file_path)
    
def send_margin_report(data_number=7):
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)    
    trading_data = pd.DataFrame()
    trading_data['日期'] = None
    trading_data['融券(張)'] = None
    trading_data['融資金額(億)'] = None
    
    # 抓取近期融資餘額資訊
    while len(trading_data)<data_number:
        today_data = get_margin(today)
        if today_data:
            trading_data.loc[len(trading_data)] = today_data
        elif len(trading_data)==0:
            return
        today -= timedelta(days=1)
    
    # 創建圖片
    file_path='plot.png'
    create_margin_jpg(trading_data, file_path)
    
    # Line 發送通知
    msg = f"""{trading_data.index[0].strftime('%Y-%m-%d')}
融資融卷餘額變化
融券：{(trading_data.loc[trading_data.index[0], '融券(張)'])} 張
融資：{(trading_data.loc[trading_data.index[0], '融資金額(億)']):.1f} 億"""
    load_dotenv()
    send_line_notify(msg=msg, token=os.getenv("LINE_MAJOR_INVESTORS_REPORT"), img='plot.png')
    
    # 刪除圖片
    if os.path.exists(file_path):
        os.remove(file_path)
    return

if __name__ == "__main__":
    send_margin_report(data_number=20)