from TW_stock_class import get_all_stock_without_class
from datetime import datetime, timedelta
import pandas as pd
import requests
import os

"""用來取得法人買賣資料"""
TW_STOCK_CSV_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../data/mi_movements_csv" 

def get_mi_movement_from_twse(start_date:str, end_date:str, stock_code:list[str]) -> dict[str:pd.DataFrame]:

    """Get major investors movements dataframe during date"""

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    result_dict = {}
    for code in stock_code:
        result_dict[code] = pd.DataFrame()
    fail_list = []
    current_date = start
    while current_date <= end:
        try:
            date_str = current_date.strftime("%Y%m%d")
            
            url = f"https://www.twse.com.tw/rwd/zh/fund/T86?response=json&date={date_str}&selectType=ALL"
            response = requests.get(url)
            data = response.json()
            
            if "data" in data:
                df = pd.DataFrame(data["data"], columns=data["fields"])
                for code in stock_code:
                    if not df[df["證券代號"].astype(str) == code].empty:
                        df_filtered = df[df["證券代號"].astype(str) == code].copy()
                        df_filtered.loc[:, "日期"] = current_date.strftime("%Y-%m-%d")
                        result_dict[code] = pd.concat([result_dict[code], df_filtered], ignore_index=True)
        except:
            fail_list.append(current_date)
            print(f"該日缺失:{current_date}")
        
        current_date += timedelta(days=1)

    while fail_list:
        try:
            current_date = fail_list[0]
            print(f"重新抓取 : {current_date} 資料")
            date_str = current_date.strftime("%Y%m%d")
            url = f"https://www.twse.com.tw/rwd/zh/fund/T86?response=json&date={date_str}&selectType=ALL"
            response = requests.get(url)
            data = response.json()
            if "data" in data:
                df = pd.DataFrame(data["data"], columns=data["fields"])
                for code in stock_code:
                    if not df[df["證券代號"].astype(str) == code].empty:
                        df_filtered = df[df["證券代號"].astype(str) == code].copy()
                        df_filtered.loc[:, "日期"] = current_date.strftime("%Y-%m-%d")
                        result_dict[code] = pd.concat([result_dict[code], df_filtered], ignore_index=True)
                fail_list.pop(0)
        except:
            print(f"該日缺失:{current_date}")
    return result_dict

def save_mi_movement_to_csv(df_dict:dict[str:pd.DataFrame]) -> None:

    """Save major investors movements dataframe to csv"""
    
    stock_code = list(df_dict.keys())
    for code in stock_code:
        if not df_dict[code].empty:
            df_dict[code]["日期"] = pd.to_datetime(df_dict[code]["日期"])
            df_dict[code].sort_index(inplace=True)
            df_dict[code].to_csv(f"{TW_STOCK_CSV_PATH}/{code}_mi_movement.csv", encoding="utf-8", index=False)
            print(f"Save to : {TW_STOCK_CSV_PATH}/{code}_mi_movement.csv")
    return

def read_mi_movements_from_csv(code:str, start_date:str, end_date:str) -> pd.DataFrame:

    """
    Read major investors movements from csv durning these days

    Parms :
        code : Code of stock (ex. 2330)
        start_date : The date you want to observe begin
        end_date : end of the date
    
    Examples : 
    ```
        data = read_mi_movements_from_csv(code="2330", start_date="2023-01-01", end_date="2023-01-02")
    ```
    """

    file_path = f"{TW_STOCK_CSV_PATH}/{code}_mi_movement.csv"
    df = pd.read_csv(file_path)
    df.set_index('日期', inplace=True)
    df.rename_axis('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[df.index <= end_date]
    df = df[start_date <= df.index ]
    return df

if __name__ == "__main__":
    start_date = "2018-01-02"
    end_date = "2024-07-04"
    all_stock = get_all_stock_without_class()
    for i in range(len(all_stock)):
        all_stock[i] = all_stock[i].split(".")[0]
    stocks_mi_movements = get_mi_movement_from_twse(start_date, end_date, all_stock)
    save_mi_movement_to_csv(stocks_mi_movements)


