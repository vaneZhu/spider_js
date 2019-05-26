from pprint import pprint

import requests

if __name__ == '__main__':
 url = 'https://www.xiaohongshu.com/wx_mp_api/sns/v1/homefeed?oid=travel&page=1&page_size=20'
 response = requests.get(url)
 # pprint(response.json())
 pprint([(item['title'],item['likes'],item['user']['nickname'])for item in response.json()['data']])
