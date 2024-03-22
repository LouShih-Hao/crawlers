import requests as rq
import pprint
import re
import json
import os
from datetime import datetime as dt
from datetime import timedelta as td


result = {}
result['觀測站'] = 'AQI'
current_time = dt.now()
previous_hour_time = (current_time - td(hours=1)).strftime('%Y%m%d%H')
url = 'https://airtw.moenv.gov.tw/json/camera_ddl_pic/camera_ddl_pic_{}.json'.format(previous_hour_time)
r = rq.get(url)

if r.status_code == rq.codes.ok:
    data = r.json()
    # pprint.pprint(data)

    for d in data:
        name = d['Name']
        if 'AQI' not in name or not bool(re.search(r'(\d+)', name)):
            continue
        analysis = re.search(r'(.+)\(AQI=(\d+)', name)
        site = analysis.group(1)
        aqi = analysis.group(2)
        # print(site, aqi)
        result[site] = aqi

    print(result)
json_data = json.dumps(result, sort_keys=False, indent=1)
folder = './datas_of_aqi/'
filename = '{}_the_data_of_aqi.json'.format(previous_hour_time)
path = os.path.join(folder, filename)

with open(path,'w') as f:
    f.write(json_data)
    print('Save the json file {}'.format(previous_hour_time))