from pprint import pprint

import requests

if __name__ == '__main__':
 url = 'https://app.zhuanzhuan.com/zzopen/sellbook/newBookList?pageNum=1&pageSize=20'
 response = requests.get(url)
 # pprint(response.json())
 pprint([(item['isbn13'],item['title'],item['authors'],item['sellPrice']/100) for item in response.json()['respData']['list']])
