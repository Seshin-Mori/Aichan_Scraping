import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import re

# URLの処理を行う関数
def process_url(target_url):
    response = requests.get(target_url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="tab")
    race_differences = []

    for idx, div in enumerate(divs, start=1):
        race_name = div.find("h3", {"id": f"toc{idx}_headline_1"}).text
        table = div.find("table")
        rows = table.tbody.find_all("tr")

        tr_5_value = float(rows[4].find_all("td")[2].text)
        tr_6_value = float(rows[5].find_all("td")[2].text)

        difference = round(tr_5_value - tr_6_value, 4)
        race_differences.append((race_name, difference))

    return race_differences

# 日時の取得とURLの生成
now = datetime.now(pytz.timezone('Asia/Tokyo'))
formatted_date = now.strftime('%Y/%m/%Y%m%d')
base_url = "https://www.aichan-engineer.com/"
min_xx = 1
max_xx = 99

all_race_differences = []

# 数値が入らないパターン
target_url = f"{base_url}{formatted_date}-ai.html"
all_race_differences += process_url(target_url)

# 数値が入るパターン
for i in range(min_xx, max_xx + 1):
    target_url = f"{base_url}{formatted_date}-ai_{i:02}.html"
    all_race_differences += process_url(target_url)

# すべての要素を差分が多い順に並べ替える
all_race_differences.sort(key=lambda x: x[1], reverse=True)

# 並び替えた結果を出力する
for race_name, difference in all_race_differences:
    print(f"レース名：{race_name}")
    print(f"差分：{difference:.4f}")

print(f"\n{len(all_race_differences)} 件のレースが処理されました。")
