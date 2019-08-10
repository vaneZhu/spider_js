from pprint import pprint

import pandas as pd
import requests

from lxml import etree
def get_goods_items(url):
    response = requests.get(
        url,verify=False)
    xml = etree.HTML(response.text)
    goods_items = xml.xpath('//li[@class="gl-item"]')
    goods_infos = pd.DataFrame()
    for goods_item in goods_items:
        goods_name = ''.join(goods_item.xpath('.//div[contains(@class,"p-name")]//em//text()')).strip()
        jd_sku = ''.join(goods_item.xpath('.//div[contains(@class,"j-sku-item")]/@data-sku'))
        jd_shop = ''.join(goods_item.xpath('.//div[contains(@class,"j-sku-item")]/@jdzy_shop_id'))
        goods_infos = goods_infos.append(
            pd.Series([goods_name, jd_sku, jd_shop], index=['goods_name', 'jd_sku', 'jd_shop']), ignore_index=True)
    return goods_infos

def get_goods_info(sku_infos):
    sku_df = pd.DataFrame()
    for i in range(len(sku_infos) // 5 + 1):
        tmp_skus = sku_infos[i * 5:(i + 1) * 5]
        if tmp_skus:
            response = requests.get('https://p.3.cn/prices/mgets?skuIds={}'.format(','.join(tmp_skus)), verify=False)
            sku_df = sku_df.append(pd.DataFrame(
                [{'jd_sku': item['id'].split('_')[-1], 'jd_price': item['p']} for item in response.json()]),
                                   ignore_index=True)
    return sku_df

def get_manjian_quan(sku_id,shop_id,jdPrice,category1_code,category2_code,category3_code):
    s = pd.Series([sku_id,""],index=['jd_sku','满减券'])
    data = {'skuId': sku_id,
            'area': '1_72_2799_0',
            'shopId': shop_id,
            'cat': '{},{},{}'.format(category1_code,category2_code,category3_code),
            'jdPrice':jdPrice
            }
    response = requests.get(
        'https://cd.jd.com/promotion/v2?{}'.format('&'.join('{}={}'.format(k, v) for k, v in data.items())),
        verify=False, )
    pickTags = response.json().get('prom',{}).get('pickOneTag')
    if len(pickTags)>0:

        c = pickTags[0].get('content', "").strip()
        if c.startswith('满'):
            s['满减券'] = c
            return s

    return s


def get_manjian_quans(datas):
    quan_df = pd.DataFrame()

    for data in datas:
        # print(data)
        quan_df=quan_df.append(get_manjian_quan(**data),ignore_index=True)
    return quan_df

if __name__ == '__main__':
    print('\n'*10)
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', 30)
    requests.packages.urllib3.disable_warnings()
    category_1_code = "9987"
    category_2_code = "653"
    category_3_code = "655"
    url =  'https://list.jd.com/list.html?cat={}&page=2&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=10#J_main'.format(','.join([category_1_code,category_2_code,category_3_code]))
    print(url)
    goods_items = get_goods_items(url)
    print('商品列表请求完毕')
    sku_ids=[goods_items.iloc[index]['jd_sku']for index in goods_items.index]
    # print(sku_ids)
    sku_items = get_goods_info(sku_ids)
    print('商品详情请求完毕')
    df = pd.merge(sku_items,goods_items,on='jd_sku')
    quan_ids = [{'sku_id':df.iloc[index]['jd_sku'],
                 'shop_id':df.iloc[index]['jd_shop'],
                 'category1_code':category_1_code,
                 'category2_code':category_2_code,
                 'category3_code':category_3_code,
                 'jdPrice':df.iloc[index]['jd_price']
                 } for index in df.index]
    print('满减券请求完毕')
    quan_df = get_manjian_quans(quan_ids)
    df = pd.merge(df,quan_df,on='jd_sku')
    assert isinstance(df,pd.DataFrame)
    df = df[df['满减券'].str.len()>0]
    print(df.loc[:,['jd_price','满减券','goods_name']].head(5))