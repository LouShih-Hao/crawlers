import requests
from bs4 import BeautifulSoup as bs

root_url = 'https://disp.cc'

r = requests.get('https://disp.cc/b/PttHot')
soup = bs(r.text, 'html.parser')
# spans = soup.find_all('span', class_='L34 nowrap listTitle')
# for span in spans:

#     # print(span.find('a').get('href'))
#     # print(span.find('a')['href'])

#     id_no = span.find('a').get('id')
#     url = root_url + span.find('a').get('href')
#     title = span.text
#     if id_no == 'link65059':
#         continue
#     print(url + '\t' + title)

# CSS Selector 的寫法
# div 裡面的span
spans = soup.select('div#list span.L34.nowrap.listTitle')
for span in spans:

    id_no = span.find('a').get('id')
    url = root_url + span.find('a').get('href')
    title = span.text
    if id_no == 'link65059':
        continue
    print(url + '\t' + title)