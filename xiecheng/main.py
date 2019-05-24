import jsonpickle
import requests
import time
import re
import execjs
import os
import datetime

import json

from xiecheng.util import base64encode, base64decode
from lxml import etree

os.environ['EXECJS_RUNTIME'] = 'Node'


class XieCheng():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': '0',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
    }
    # cookies = {
    #     '_zQdjfing': '275ad065b02e5fa4cc5fa4cc3165bb4ea084d5c0863365ac5fa4cc',
    #     'fcerror': '693370523',
    # }

    def __init__(self, roomid, cityid=2):
        '''
        :param roomid: hotalid
        :param cityid: cityid 为1是北京，为2是上海
        '''
        self.cityid = cityid
        self.roomid = roomid
        url = 'https://hotels.ctrip.com/domestic/hotel/{}.html'.format(roomid)
        print(url)
        self.session = requests.Session()
        # self.session.proxies={'https':'socks5://39.97.77.27:1080','http':'socks5://39.97.77.27:1080'}
        self.session.headers.update(self.headers)
        self.session.verify = False
        self.address = ''.join(
            [item.strip() for item in etree.HTML(self.session.get(url).text).xpath('//div[@class="adress"]//text()') if
             item.strip()])

        self.session.cookies.update(self.get_cookies(str(roomid)))
        self.session.cookies.update({'hoteluuid':'FLPsulDO87oZ2MnZ'})
        self.session.headers.update({'Referer': url})
        self.url = url
        self.call_back_value = 'CASrYVcraFQgjGciKk'
        self.start_date = datetime.date.today()
        self.dep_date = (datetime.timedelta(days=1) + self.start_date)
        self.init_font_map()

    def get_cookies(self,text):
        with open('cookies.js',encoding='utf-8') as fr:
            # print(text)
            cookies = execjs.compile(fr.read()).call('get_cookies', text)
            print(cookies)

            return cookies

    def __del__(self):
        self.session.close()


    def eleven_js_decorator(self, fun):
        def __decorator(*args, **kwargs):
            eleven_js = fun(*args, **kwargs)
            try:
                print(eleven_js)
                b64_eleven_js = base64encode(eleven_js)
                b64_url = base64encode(self.url)
                url = 'http://127.0.0.1:3000/get_eleven'
                response = requests.post(url, data={'text': b64_eleven_js, 'url': b64_url})
                return base64decode(response.text)
            except Exception as e:
                msg = '%s' % e
                # print(msg)
                if 'navigator' in msg:
                    raise Exception('ip 被封了，请更换ip或稍后重试')
                raise e

        return __decorator

    def get_eleven_js(self):
        url = 'http://hotels.ctrip.com/domestic/cas/oceanball?callback={}&_={}'.format(self.call_back_value,
                                                                                       self.get_ms())
        response = self.session.get(url=url)
        return response.text

    def get_eleven(self):
        eleven_js = self.eleven_js_decorator(self.get_eleven_js)()
        return eleven_js

    def get_ms(self):
        return int(time.time() * 1000)

    def get_room(self):
        eleven = self.get_eleven()
        print(eleven)
        url = 'https://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx'
        params = {'psid': '',
                  'MasterHotelID': self.roomid,
                  'hotel': self.roomid,
                  'EDM': 'F',
                  'roomId': '',
                  'IncludeRoom': '',
                  'city': self.cityid,
                  'showspothotel': 'T',
                  'supplier': '',
                  'IsDecoupleSpotHotelAndGroup': 'F',
                  'contrast': '0',
                  'brand': '0',
                  'startDate': str(self.start_date),
                  'depDate': str(self.dep_date),
                  'IsFlash': 'F',
                  'RequestTravelMoney': 'F',
                  'hsids': '',
                  'IsJustConfirm': '',
                  'contyped': '0',
                  'priceInfo': '-1',
                  'equip': '',
                  'filter': '',
                  'productcode': '',
                  'couponList': '',
                  'abForHuaZhu': '',
                  'defaultLoad': 'T',
                  'esfiltertag': '',
                  'estagid': '',
                  'Currency': '',
                  'Exchange': '',
                  'TmFromList': 'F',
                  'RoomGuestCount': '1,1,0',
                  'eleven': eleven,
                  'callback': self.call_back_value,
                  '_': self.get_ms()}
        return self.session.get(url, params=params)

    def run(self):
        response = self.get_room()
        # print(response.json())
        b64_font = base64encode(json.dumps(response.json()))
        # print(b64_font)
        html_content = base64decode(self.font_js.call('parser', b64_font))
        # html_content=response.json()['html'] 直接使用返回的html，价格不对。
        self.parser(html_content)
        with open('xiecheng.html', 'w', encoding='utf-8') as fw:
            html_content='''<html><head><meta charset="UTF-8"></head><body>{}</body></html>'''.format(html_content)
            fw.write(html_content)


    def parser(self, html_content):
        print('{} 房间分布已经抓取，请到xiecheng.html查看'.format(self.address))
        xml = etree.HTML(html_content)
        price = xml.xpath('//*/@data-pricedisplay')
        print('真实房价',price)

    def init_font_map(self):
        with open('font_map.js', encoding='utf-8') as fr:
            self.font_js = execjs.compile(fr.read())


if __name__ == '__main__':
    # roomid=7067729
    # cityid = 2  # 上海
    # roomid = 6410223
    # cityid = 1 # 北京
    roomid = 6386846
    cityid = 1 # 北京

    XieCheng(roomid, cityid=cityid).run()
