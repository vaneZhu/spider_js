import json
import urllib.parse
from hashlib import md5,sha256
import requests
def sign( url, data):
    querys = urllib.parse.unquote_plus(urllib.parse.urlparse(url).query) + '&' + urllib.parse.unquote_plus(
        urllib.parse.urlencode(data))
    to_sign = ''.join(sorted(querys.split('&')))
    signed = md5('{}{}'.format(to_sign, '382700b563f4').encode('utf-8')).hexdigest()
    token_signed = sha256('{}{}'.format(signed, '57039b18e851459c412b2265da22d2f9').encode('utf-8')).hexdigest()
    return {'sig': signed, '__NStokensig': token_signed}
if __name__ == '__main__':
    home_url = 'http://api.gifshow.com/rest/n/feed/profile2?did=ANDROID_dbb266ac63b34bec&appver=6.3.4'

    formdata = {'client_key': '3c2cd3f3','user_id':'694118297'}
    formdata.update(sign(home_url,formdata))
    # headers={'User-Agent':"kwai-android"}
    response = requests.post(home_url,data=formdata)
    print(json.dumps(response.json(),ensure_ascii=False))
