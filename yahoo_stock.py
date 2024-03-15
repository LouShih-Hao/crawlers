import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://tw.stock.yahoo.com/quote/2330.TW')

if r.status_code == requests.codes.ok:
    soup = bs(r.text, 'html.parser')
    ul = soup.find_all('ul', class_='D(f) Fld(c) Flw(w) H(192px) Mx(-16px)')[0]
    print(ul)

    price = ul.find_all('span')[1]
    print(price.text)

    