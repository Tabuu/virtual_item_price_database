import re
import json
import requests

from bs4 import BeautifulSoup
from selenium import webdriver


firefox_option = webdriver.FirefoxOptions()
firefox_option.headless = False


def buff_csgo_goods(buff_item_id):
    driver = webdriver.Firefox(options=firefox_option)
    driver.get(f'https://buff.163.com/market/goods?goods_id={buff_item_id}#tab=buying')

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    ref_price_div = soup.find('div', {'class': 'detail-cont'}).find('strong', {'class': 'f_Strong'})
    match = re.search(r"^¥\s(\d+)\.?(\d*)", ref_price_div.text)
    ref_price = int(match.group(1) + match.group(2).ljust(2, '0'))

    price_text = soup.find("table", {"class": "list_tb"}).find_all("tr")[1].find('p', {'class': 'hide-cny'})
    min_sell_price = int(float(price_text.text[3:-1]) * 100)

    driver.close()

    return {
        'lowest_price': min_sell_price,
        'reference_price': ref_price
    }


def steam_csgo_price_overview(steam_item_id):
    response = requests.get(
        f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={steam_item_id}")
    data = json.loads(response.text)

    median_price = int(float(data['median_price'][0:-1].replace(',', '.')) * 100)
    lowest_price = int(float(data['lowest_price'][0:-1].replace(',', '.')) * 100)
    volume = int(data['volume'].replace(',', ''))

    return {
        'lowest_price': lowest_price,
        'median_price': median_price,
        'volume': volume
    }


def is_valid_buff_item_id(buff_item_id, steam_item_id):
    response = requests.get(
        f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={steam_item_id}")
    data = json.loads(response.text)

    if not data['success']:
        return False

    driver = webdriver.Firefox(options=firefox_option)
    driver.get(f'https://buff.163.com/market/goods?goods_id={buff_item_id}')

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    item_name = soup.find('span', {'class': 'cru-goods'}).text

    is_valid = item_name == steam_item_id
    print(item_name, steam_item_id, driver.title)

    driver.close()

    return is_valid
