import requests
from lxml import etree

from leisong.sign import sign
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
jieba.load_userdict("words.txt")
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

}
with open('stop.txt',encoding='utf-8') as fr:
    stop_words = [word.strip()for word in fr.readlines() if word.strip()]

def download(url,method="GET",headers=headers,**kwargs):
    response = requests.request(method,url,headers=headers,**kwargs)
    return response

def parser(content,rule):
    xml = etree.HTML(content)
    return xml.xpath(rule)

def get_song_links(url):
    response  = download(url)
    urls = parser(response.content,'//div[@id="hotsong-list"]//li/a/@href')
    return urls

def get_lyric(song_id):
    lyric_url = 'https://music.163.com/weapi/song/lyric?csrf_token='
    datas = sign({"id": song_id, "lv": -1, "tv": -1})
    response = download(lyric_url, method='POST', data=datas)
    return '\n'.join([line.split(']')[-1]for line in response.json()['lrc']['lyric'].split('\n')])

def cut_words(datas):
    words = {}
    for data in datas:
        for line in data.split('\n'):
            tmps = jieba.cut(line)
            # print(stop_words,'==')
            tmps = [tmp for  tmp in tmps if tmp.strip() and tmp.strip() not in stop_words]
            for word in tmps:
                words[word]=words.setdefault(word,1)+1
    words = sorted(words.items(),key=lambda item:item[1],reverse=True)
    return dict(words)

def gen_word_cloud(words):
    wordcloud = WordCloud(font_path='fonts/youyuan.TTF').generate_from_frequencies(words)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

def main():
    home_url =  'https://music.163.com/artist?id=6731'
    sub_urls = get_song_links(home_url)
    song_ids = [sub_url.split('=')[-1]for sub_url in sub_urls]
    lyrics = [get_lyric(song_id)for song_id in song_ids]
    words = cut_words(lyrics)
    gen_word_cloud(words)





if __name__ == '__main__':
    main()

