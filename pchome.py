import requests as rq
import pprint


page = 1
count = 0

while True:
    url = f'https://ecshweb.pchome.com.tw/searchplus/v1/index.php/all/category/DHAAOS/results?show=list&page={page}&pageCount=40'
    r = rq.get(url)

    if r.status_code == rq.codes.ok:
        data = r.json()
        if page > data['totalPage']:
            break
        for product in data['prods']:
            print(product['name'])
            print(product['price'])
            count += 1
    page += 1

print(f'共有{count}筆資料被查詢')
