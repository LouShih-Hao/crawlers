from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

base_url = 'https://www.dcard.tw/f/mood/p/254935478'
data = {}

# 初始化WebDriver
driver = webdriver.Edge()

# 設定等待網頁載入的時間
driver.implicitly_wait(10)

# 連線到網站
driver.get(base_url)

time.sleep(10)

# 取得網頁內容
html = driver.page_source

soup = bs(html, 'html.parser')

ld_json = soup.find_all('script', type='application/ld+json')
ele = ld_json[-1]
context = ele.text
print(context)

# 抓回文總筆數
start_position = context.find('"commentCount":')
pattern_len = len('"commentCount":')
end_position = context.find('},{"@context"')
print(start_position)
print(end_position)
commentCount = int(context[start_position + pattern_len : end_position])

# 關閉WebDriver, 瀏覽器也會跟著關閉
driver.quit()

for i in range(commentCount):
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    driver.get(base_url + '/b/' + str(i+1))
    time.sleep(10)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    span = soup.find('span', class_='atm_vv_1q9ccgz atm_sq_1l2sidv atm_ks_15vqwwr atm_7l_5io6hg tygfsru')
    if span is None:
        continue
    div = soup.find('div', class_='atm_vv_1btx8ck atm_w4_1hnarqo c1ehvwc9')
    if div is None:
        continue
    if span.text not in data.keys():
        data[span.text] = [div.text]
    else:
        data[span.text].append(div.text)
    driver.quit()

print(data)
sorted_data = sorted(data.items(), key=lambda x: len(x))
print(sorted_data)