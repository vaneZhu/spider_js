import os
import uuid

import requests
from lxml import etree

from kuaishou.fontutils.models import Font
from kuaishou.settings import FONTS
import re
import hashlib

def md5(text:str):
    md = hashlib.md5()
    # text = isinstance()
    if not isinstance(text,bytes):
       text= str(text).encode('utf-8')
    md.update(text)
    return md.hexdigest()

default_font = Font(path=FONTS['path'], font_map=FONTS['font_map'])

class KuaiShouSpider():
    def __init__(self):
        self.session = requests.Session()

    def download(self,url):
        return self.session.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Rerfer':url})

    def get_remote_font(self,url):
        response = self.download(url)
        state,html = response.status_code,response.content
        if state==200:
            print('{}.ttf'.format(md5(url + uuid.uuid4().hex)))
            _temp = os.path.join(os.path.dirname(FONTS['path']),'{}.ttf'.format(md5(url + uuid.uuid4().hex)))
            with open(_temp,'wb') as fw:
                fw.write(html)
                file_sign=md5(html)
            f = Font(_temp)
            # os.remove(_temp)
            return f,file_sign
        else:
            raise Exception('download remote font faile:{}'.format(url))

    def fixed_font(self, url,home_response):
        remote_font, file_sign = self.get_remote_font(url)
        f_html = home_response.text
        f_html, xml = self.fixed_one(f_html, remote_font)
        numbers = self.fixed_next(f_html, xml)
        # f_html = self.remove_script(f_html)
        return numbers

    def remove_script(self, f_html):
        clear = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
        f_html = clear.sub("", f_html)
        return f_html

    def fixed_next(self, f_html, xml):
        numbers = re.findall('"watchingCount":\s*"(.*?)"', f_html, re.I | re.S)
        print(numbers)
        return numbers

    def fixed_one(self, f_html, remote_font):
        xml = etree.HTML(f_html)
        numbers = re.findall('"watchingCount":\s*"(\w+)"', f_html, re.I | re.S)
        fonts = set([item for item in ''.join(numbers)])
        uni_numbers = {("UNI" + item.encode('unicode_escape').decode('utf-8')[2:]).upper(): item.strip() for item in
                       fonts}
        for uni_number, default_value in uni_numbers.items():
            contour = remote_font.uni_to_contour.get(uni_number)
            number = default_font.contour_to_font.get(contour)
            if number is not None:
                f_html = re.sub(default_value, str(number), f_html, flags=re.S | re.I)
        return f_html, xml

    def run(self,url):
        print(url)
        home_response  = self.download(url)
        matcher = re.search("https://static.yximgs.com/udata/pkg/kuaishou-front-end-live/.*?ttf", home_response.text)
        if matcher:
            font_url = matcher.group()
            numbers= self.fixed_font(font_url,home_response)
            self.parser(home_response.content,numbers)

        else:
            raise Exception('not found font_url')

    def parser(self, fixed_html,numbers):
        xml = etree.HTML(fixed_html)
        names = [name.strip()for name in xml.xpath('//ul[@class="live-card-list"]/li//a[@class="user-info has-current-watching"]//text()')]
        for name,watching_count in list(zip(names,numbers))[:19]:
            print(name,watching_count)
            pass


if __name__ == '__main__':
    url = 'https://live.kuaishou.com/cate/DQRM/'
    KuaiShouSpider().run(url)