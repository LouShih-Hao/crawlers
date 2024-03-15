import requests as rq
import os
import json
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from datetime import timedelta as td
from multiprocessing import Pool
from multiprocessing import Process


def save_to_json(date, data):
    json_data = json.dumps(data, sort_keys=False, indent=1)
    folder = './datas_of_future/'
    filename = '{}_the_data_of_future.json'.format(date)
    path = os.path.join(folder, filename)

    with open(path,'w') as f:
        f.write(json_data)
        print('Save the json file {}'.format(date))

def crawl(date):
    url = 'https://www.taifex.com.tw/cht/3/futContractsDate'
    q_condition = f'queryType=1&doQuery=1&queryDate={date.year}%2F{date.month}%2F{date.day}'
    title_parts = []
    title = ['商品名稱', '身分別']
    data = {}
    date_to_save = date.strftime('%Y-%m-%d')

    print('The datas of date', date.strftime('%Y/%m/%d'), 'crawling')
    r = rq.get(url + '?' + q_condition)

    if r.status_code == rq.codes.ok:
        soup = bs(r.text, 'html.parser')
    else:
        print('Connection error!')

    try:
        table = soup.find('table', class_='table_f')
        trs = table.find_all('tr')
    except AttributeError:
        print('No data for', date.strftime('%Y/%m/%d'))
        return
    
    for i in range(3):
        result = []
        if i == 2:
            ths = trs[i].find_all('th', attrs={'align':'right'})
        else:
            ths = trs[i].find_all('th')
        for th in ths:
            if th.text in result:
               continue
            result.append(th.text)
        title_parts.append(result)
    
    for i in range(len(title_parts[0])):
        for j in range(len(title_parts[1])):
            for k in range(len(title_parts[2])):
                title.append(title_parts[0][i] + '-' + title_parts[1][j] + '-' + title_parts[2][k])

    for tr in trs[3:len(trs)-4]:
        ths = tr.find_all('th')
        if len(ths) > 1:
            t_product = ths[1].text.strip()
            t_identity = ths[2].text.strip()
        else :
            t_identity = ths[0].text.strip()
        tds = tr.find_all('td')
        cells = [int(td.text.strip().replace(',', '')) for td in tds]

        row_data = [t_product] + [t_identity] + cells

        product = row_data[0]
        identity = row_data[1]
        price = {title[i] : row_data[i] for i in range(2, len(title))}

        if product not in data:
            data[product] = {identity: price}
        else:
            data[product][identity] = price

    # print(data['臺股期貨']['外資']['未平倉餘額-多空淨額-口數'])
    save_to_json(date_to_save, data)

def main():
    start = time.time()
    date_ori = dt.today()
    date = date_ori
    futures = {}
    with Pool(os.cpu_count()) as pool:
        while True:
            pool.apply_async(crawl, args=(date,))
            date -= td(days=1)
            if date < date_ori - td(days=731):
                break
        pool.close()
        pool.join()
    end = time.time()
    print(f'執行本程式共花費{end - start}秒')

if __name__ == '__main__':
    main()