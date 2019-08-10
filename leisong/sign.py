import json
from Crypto.Cipher import AES
import base64
import binascii


def aes(text,key):
    pad = 16 - len(text)%16
    text = text + pad * chr(pad)
    text = text.encode()
    encryptor = AES.new(key,AES.MODE_CBC,''.join(['0{}'.format(i) for i in range(1,9)]))
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode()


def rsa(random,public_key,data):
    rsa = int(binascii.hexlify(random), 16) ** int(public_key, 16) % int(data, 16)
    return format(rsa, 'x').zfill(256)


def sign(data):
    random = '1' * 16
    text = json.dumps(data)
    params = aes(text,'0CoJUm6Qyw8W8jud')
    params = aes(params,random)
    encSecKey = rsa(random.encode(),"010001",'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7')
    return  {'params':params,
             'encSecKey':encSecKey  }
if __name__ == '__main__':
    print(sign({}))