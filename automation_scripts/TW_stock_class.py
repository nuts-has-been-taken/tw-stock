from typing import Optional
from bs4 import BeautifulSoup
import requests
import json
import os

"""這是用來爬取目前台股的所有股票(無興櫃)，資料來源為 yahoo股市"""
# TODO : yahoo股市沒有提供興櫃的股票分類和代號，但是 yfinance 爬的到，需要去其他地方抓

BASE_YAHOO_URL = "https://tw.stock.yahoo.com"
TW_STOCK_CLASS_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../data/tw_stock_list_json/TW_stock_list.json" 

def load_TW_stock_json():
    try:
        with open(TW_STOCK_CLASS_PATH, 'r') as file:
            tw_data = json.load(file)
    except Exception as e:
        print(f"Error msg : {e}")
        print("Please make sure you have download the TW_stock_list.json first, it should be in the json_file folder !")
        return None
    return tw_data

def get_all_stock_without_class() -> Optional[list]:

    """Return list of all TW stock"""

    tw_data = load_TW_stock_json()
    
    all_stock = []
    for type_class in list(tw_data.keys()):
        listed_stock = tw_data[type_class]
        for class_ in list(listed_stock.keys()):
            if class_ != "分類":
                all_stock.extend(listed_stock[class_]["class_stock_number"])
    all_stock = list(set(all_stock))
    return all_stock

def get_stocks_by_class(class_name:str) -> dict[str:list]:

    """
    Return stocks in the class

    Examples : 
    ```
        print(get_stocks_by_class(class_name="食品"))
        {
            "食品" : ["1201.TW", "1203.TW", ...],
            "櫃食品" : ["1264.TWO", "1796.TWO", ...],
        }
        print(get_stocks_by_class(class_name="Apple"))
        {
            "Apple Pay" : [...],
            "Apple watch" : [...],
            "Apple iTV" : [...],
        }
    ```
    """
    filter_stock = {}
    tw_data = load_TW_stock_json()

    for type_class in list(tw_data.keys()):
        listed_stock = tw_data[type_class]
        for class_ in listed_stock["分類"]:
            if class_name in class_:
                filter_stock[class_] = listed_stock[class_]["class_stock_number"]
    return filter_stock

def save_record(json_records:json, name:str):

    """將 yahoo股市 爬取到的類股資料存進 json 檔"""

    with open(f'../json_file/{name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_records, json_file, indent=4, ensure_ascii=False)
    return

def get_from_class(url:str):

    """爬取該種類的所有股票名稱和編號"""

    class_number = []
    class_info = {}
    class_stok_info = requests.get(f"{BASE_YAHOO_URL}{url}")
    class_soup = BeautifulSoup(class_stok_info.content, "html.parser")
    all_stock = class_soup.find("div", class_="table-body-wrapper").find_all("li", class_="List(n)")
    for stock in all_stock:
        stock_name_component = stock.find("div", class_="Lh(20px) Fw(600) Fz(16px) Ell")
        if stock_name_component:
            stock_name = stock_name_component.text
        else:
            stock_name = stock.find("div", class_="Lh(20px) Fw(600) Fz(14px) Ell").text
        stock_number = stock.find("span", class_="Fz(14px) C(#979ba7) Ell").text
        class_number.append(stock_number)
        class_info[stock_number]=stock_name
    return class_number, class_info

def class_crawler():

    """爬取所有類股資料"""

    json_records = {}

    base_url = f"https://tw.stock.yahoo.com/class/"
    yahoo_stock = requests.get(base_url)
    soup = BeautifulSoup(yahoo_stock.content, "html.parser")

    # get listed stock class name
    listed_stock_class = []
    listed_stock_json = {}
    listed_stock = soup.find("div", id="LISTED_STOCK").find("ul").find_all("a")

    for class_stock in listed_stock:
        class_name = class_stock.text
        listed_stock_class.append(class_name)

        # get all stock in the class
        class_stock_number, class_stock_info = get_from_class(class_stock.get("href"))
        class_stock_json = {
            "class_stock_number":class_stock_number,
            "class_stock_info":class_stock_info
        }
        listed_stock_json[class_name] = class_stock_json
    listed_stock_json["分類"] = listed_stock_class
    json_records["上市類股"] = listed_stock_json

    # get over the counter stock
    otc_stock_class = []
    otc_stock_json = {}
    otc_stock = soup.find("div", id="OVER_THE_COUNTER_STOCK").find("ul").find_all("a")
    for class_stock in otc_stock:
        class_name = class_stock.text
        otc_stock_class.append(class_stock.text)

        # get all stock in the class
        class_stock_number, class_stock_info = get_from_class(class_stock.get("href"))
        class_stock_json = {
            "class_stock_number":class_stock_number,
            "class_stock_info":class_stock_info
        }
        otc_stock_json[class_name] = class_stock_json
    otc_stock_json["分類"] = otc_stock_class
    json_records["上櫃類股"] = otc_stock_json

    # get electric stock
    electric_stock_class = []
    electric_stock_json = {}
    electric_stock = soup.find("div", id="ELECTRONICS_INDUSTRY").find("ul").find_all("a")
    for class_stock in electric_stock:
        class_name = class_stock.text
        electric_stock_class.append(class_stock.text)

        # get all stock in the class
        class_stock_number, class_stock_info = get_from_class(class_stock.get("href"))
        class_stock_json = {
            "class_stock_number":class_stock_number,
            "class_stock_info":class_stock_info
        }
        electric_stock_json[class_name] = class_stock_json
    electric_stock_json["分類"] = electric_stock_class
    json_records["電子產業"] = electric_stock_json

    # get concept stock
    concept_stock_class = []
    concept_stock_json = {}
    concept_stock = soup.find("div", id="CONCEPT_STOCK").find("ul").find_all("a")
    for class_stock in concept_stock:
        class_name = class_stock.text
        concept_stock_class.append(class_stock.text)

        # get all stock in the class
        class_stock_number, class_stock_info = get_from_class(class_stock.get("href"))
        class_stock_json = {
            "class_stock_number":class_stock_number,
            "class_stock_info":class_stock_info
        }
        concept_stock_json[class_name] = class_stock_json
    concept_stock_json["分類"] = concept_stock_class
    json_records["概念股"] = concept_stock_json

    # get consortium stuck
    consortium_stock_class = []
    consortium_stock_json = {}
    consortium_stock = soup.find("div", id="CONSORTIUM_STOCK").find("ul").find_all("a")
    for class_stock in consortium_stock:
        class_name = class_stock.text
        consortium_stock_class.append(class_stock.text)

        # get all stock in the class
        class_stock_number, class_stock_info = get_from_class(class_stock.get("href"))
        class_stock_json = {
            "class_stock_number":class_stock_number,
            "class_stock_info":class_stock_info
        }
        consortium_stock_json[class_name] = class_stock_json
    consortium_stock_json["分類"] = consortium_stock_class
    json_records["集團股"] = consortium_stock_json

    # save record
    save_record(json_records, "TW_stock_list")
    print("done")

if __name__ == "__main__":
    class_crawler()