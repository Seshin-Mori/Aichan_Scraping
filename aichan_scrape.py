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
target_url = f"{base_url}{formatted_date}-ai.html"

response = requests.get(target_url)
response.raise_for_status()

# HTML parsing
soup = BeautifulSoup(response.text, "html.parser")

# Find all the divs with class "tab"
divs = soup.find_all("div", class_="tab")

for idx, div in enumerate(divs, start=1):
    print(f"レース{idx}:")
    # Extract the table from the div
    table = div.find("table")

    # Extract the table rows from the table body
    rows = table.tbody.find_all("tr")

    for row in rows:
        # Extract the horse name and jockey name from the table data
        horse_name = row.find_all("td")[4].text
        jockey_name = row.find_all("td")[5].text

        # Print the horse name and jockey name
        print(f"  馬名: {horse_name}, 騎手名: {jockey_name}")
    print()
