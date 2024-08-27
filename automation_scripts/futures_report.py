from matplotlib.ticker import FuncFormatter
from datetime import datetime, timedelta
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
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

def get_futures(date:datetime):
    url = "https://www.taifex.com.tw/cht/3/futContractsDate"
    data = {
        'queryType': '1',
        'goDay': '',
        'doQuery': '1',
        'dateaddcnt': '',
        'queryDate': date.strftime('%Y/%m/%d'),
        'commodityId': '',
        'button': '送出查詢'
    }
    
    response = requests.post(url, data=data)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find("tbody")
    if content:
        content = content.find_all("tr")
        res = {
            "日期":date,
            "自營商":eval(content[0].find_all("td", align="right")[11].text.strip().replace(',', '')),
            "投信":eval(content[1].find_all("td", align="right")[11].text.strip().replace(',', '')),
            "外資":eval(content[2].find_all("td", align="right")[11].text.strip().replace(',', '')),
        }
    else:
        return None
    
    return res

def create_futures_jpg(df:pd.DataFrame, file_path='plot.png'):
    
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
        return f'{int(value/100000000)} (億)'

    fig, ax1 = plt.subplots(figsize=(10, 6))

    bar_width = 0.5
    index = np.arange(len(dates))

    global_pos = df['外資'].clip(lower=0)
    global_neg = df['外資'].clip(upper=0)
    secu_pos = df['投信'].clip(lower=0)
    secu_neg = df['投信'].clip(upper=0)
    self_pos = df['自營商'].clip(lower=0)
    self_neg = df['自營商'].clip(upper=0)

    bar1 = ax1.bar(index, global_pos, bar_width, label='外資', color='#2894FF')
    bar2 = ax1.bar(index, secu_pos, bar_width, bottom=global_pos, label='投信', color='#B15BFF')
    bar3 = ax1.bar(index, self_pos, bar_width, bottom=global_pos + secu_pos, label='自營商', color='#FF8F59')

    ax1.bar(index, global_neg, bar_width, label='外資', color='#2894FF')
    ax1.bar(index, secu_neg, bar_width, bottom=global_neg, label='投信', color='#B15BFF')
    ax1.bar(index, self_neg, bar_width, bottom=global_neg + secu_neg, label='自營商', color='#FF8F59')

    ax1.axhline(0, color='black', linewidth=0.8, linestyle='-')
    ax1.grid(axis='y', linestyle='--', linewidth=0.7)
    ax1.set_xticks(index[::int(len(dates)/6)])
    ax1.set_xticklabels(dates[::int(len(dates)/6)].strftime('%Y-%m-%d'))
    ax1.set_xlabel('日期', rotation=0, labelpad=12)
    handles = [bar1, bar2, bar3]
    ax1.legend(handles=handles, loc="upper left")

    ax1.yaxis.set_major_formatter(FuncFormatter(format_func))

    plt.title('三大法人期貨未平倉')
    plt.savefig(file_path)
    
def send_futures_report(data_number=7):
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)    
    trading_data = pd.DataFrame()
    trading_data['日期'] = None
    trading_data['自營商'] = None
    trading_data['投信'] = None
    trading_data['外資'] = None

    # 抓取近期融資餘額資訊
    while len(trading_data)<20:
        today_data = get_futures(today)
        if today_data:
            trading_data.loc[len(trading_data)] = today_data
        elif len(trading_data)==0:
            pass
        today -= timedelta(days=1)
    
    # 創建圖片
    file_path='futures_plot.png'
    create_futures_jpg(trading_data, file_path)
    
    # Line 發送通知
    msg = f"""{trading_data.index[0].strftime('%Y-%m-%d')}
三大法人期貨未平倉
外資：{(trading_data.loc[trading_data.index[0], '外資']/100000000):.3f} 億
投信：{(trading_data.loc[trading_data.index[0], '投信']/100000000):.3f} 億
自營商：{(trading_data.loc[trading_data.index[0], '自營商']/10000):.1f} 萬"""
    load_dotenv()
    send_line_notify(msg=msg, token=os.getenv("LINE_MAJOR_INVESTORS_REPORT"), img=file_path)
    
    # 刪除圖片
    if os.path.exists(file_path):
        os.remove(file_path)
    return

if __name__ == "__main__":
    send_futures_report(data_number=20)