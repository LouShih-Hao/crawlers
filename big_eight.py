import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs

data = []
title = []
r = rq.get('https://chart.capital.com.tw/Chart/TWII/TAIEX11.aspx')
if r.status_code == rq.codes.ok:
    soup = bs(r.text, 'lxml')
    tables = soup.find_all('table', attrs={'cellpadding':'2'})
    for table in tables:
        trs = table.find_all('tr')
        for tr in trs:
            date, price1, price2 = [td.text for td in tr.find_all('td')]
            if date == '日期':
                if len(title) == 0:
                    title.append([date, price1, price2])
                continue
            data.append([date, price1, price2])

df = pd.DataFrame(data, columns=title)
df.to_csv('big_eight.csv')
