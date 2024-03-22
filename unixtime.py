from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas
import time


url = 'https://www.unixtimestamp.com/'
timestamp = '1234567890'
titles = []
datas = [[]]
result = []

driver = webdriver.Edge()

driver.get(url)

time.sleep(5)

timestamp_input = driver.find_element('id', 'timestamp')
timestamp_input.send_keys(timestamp)

convert_button = driver.find_element('xpath', '//button[@class="ui primary button"]')
convert_button.click()

time.sleep(5)

html = driver.page_source
soup = bs(html, 'html.parser')

driver.close()

table = soup.find('table', class_='ui celled definition table timestamp-results')
trs = table.find_all('tr')

for tr in trs:
    tds = tr.find_all('td')
    for td in tds:
        result.append(td.text)

for i in range(0,len(result),2):
    titles.append(result[i])
for i in range(1,len(result),2):
    datas[0].append(result[i])

print(titles)
print(datas)

df = pandas.DataFrame(datas, columns=titles)
print(df)
