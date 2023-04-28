import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import re

# 現在の日時（日本時間を取得する）
#now = datetime.now(pytz.timezone('Asia/Tokyo'))

# テスト用日時（コメントアウトを解除して使用）
test_date = '2023-04-22'
now = datetime.strptime(test_date, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Tokyo'))

formatted_date = now.strftime('%Y/%m/%Y%m%d')

base_url = "https://www.aichan-engineer.com/"

# XXの範囲を指定
min_xx = 1
max_xx = 99

skipped_count = 0

# 数値が入らないパターン
target_url = f"{base_url}{formatted_date}-ai.html"

response = requests.get(target_url)
if response.status_code == 200:
    # このループの前にこのURLを処理する（URLを処理するコードをここに追加）
    pass
else:
    skipped_count += 1

for i in range(min_xx, max_xx + 1):  # このループを追加
    target_url = f"{base_url}{formatted_date}-ai_{i:02}.html"

    response = requests.get(target_url)
    if response.status_code != 200:
        skipped_count += 1
        continue

    # HTML解析
    soup = BeautifulSoup(response.text, "html.parser")

    # クラス "tab" のdivをすべて見つける
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

    # 差分を降順に並び替える
    race_differences.sort(key=lambda x: x[1], reverse=True)

    # 並び替えた結果を出力する
    for race_name, difference in race_differences:
        print(f"レース名：{race_name}")
        print(f"差分：{difference:.4f}")

print(f"\n{skipped_count} 件のURLがスキップされました。")
