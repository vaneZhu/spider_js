import os
import time

from fontTools.ttLib import TTFont
import lxml.html
import lxml.etree
import json

from kuaishou.settings import FONTS
import hashlib

def md5(text:str):
    md = hashlib.md5()
    # text = isinstance()
    md.update(text.encode('utf-8'))
    return md.hexdigest()


class Font():
    def __init__(self,path,font_map=None,):
        self.path = path
        self.font_map = font_map
        self.contour_to_font=dict()
        self.uni_to_contour=dict()
        self.__init()


    def __init(self):
        print(self.path)
        assert os.path.exists(self.path)
        font_xml = self.load_default_font()
        self.parser_map(font_xml)
        if self.font_map:
            self.parser_contour(font_xml)

    def load_default_font(self):
        tt = TTFont(self.path)
        _temp=os.path.join(os.path.dirname(self.path),'{}.xml'.format(md5(self.path)))
        tt.saveXML(_temp)
        font_xml = lxml.etree.parse(_temp)
        # os.remove(_temp)
        return font_xml

    def parser_contour(self, font_xml):
        for k, v in self.font_map.items():
            try:
                element = font_xml.xpath('//TTGlyph[@name="{}"]'.format(k))[0]
                _pts = element.xpath('./contour/pt')
                pts=[''.join(pt.xpath('./@x'))for pt in _pts if ''.join(pt.xpath('./@on'))=='1' ]
                if not pts: continue
                contours = [str(e) for e in pts]
                self.contour_to_font[md5(json.dumps(contours))]=v
            except Exception:
                raise Exception('{}字体改版，请重新更新settings中的配置,key:{},val:{}'.format(self.path,k,v))

    def parser_map(self, font_xml):
        for element in font_xml.xpath('//TTGlyph'):
            try:
                name = ''.join(element.xpath('@name')[0])
                _pts = element.xpath('./contour/pt')
                pts = [''.join(pt.xpath('./@x')) for pt in _pts if ''.join(pt.xpath('./@on')) == '1']
                if not pts: continue
                contours = [str(e) for e in pts ]
                self.uni_to_contour[name.upper()] = md5(json.dumps(contours))
            except Exception as e:
                raise Exception('{}字体改版，请重新更新settings中的配置,error:{}'.format(self.path, e))


if __name__ == '__main__':
    print(Font(FONTS['path'],FONTS['font_map']).font_map)
    print(Font(FONTS['path'],FONTS['font_map']).contour_to_font)
    # print(Font(FONTS['path'],FONTS['font_map']).uni_to_contour)
    # print(Font(os.path.join(os.path.dirname(FONTS['path']),'fontscn_yx77i032.woff')).uni_to_contour)

