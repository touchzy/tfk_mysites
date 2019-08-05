# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:26:35 2018

@author: sr
"""
import hashlib
import requests
import json

class BaiduTranslate(object):
    '''百度api调用格式：http://api.fanyi.baidu.com/api/trans/vip/translate?q=apple&from=en&to=zh&appid=2015063000000001&salt=1435660288&sign=f89f9594663708c1605f3d736d01d2d4'''
    
    def __init__(self, translate_str):
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.q = translate_str
        self.from_ = 'zh'
        self.to_ = 'en'
        self.appid = '20190718000319027'
        self.key = '165gdtmBviFEJLNwDbYi'
        self.salt = '1994052499'
        str1 = self.appid + self.q + self.salt + self.key
        hl = hashlib.md5()
        hl.update(str1.encode(encoding='utf-8'))
        self.sign = hl.hexdigest()
        self.full_url = self.url + "?q=" + requests.utils.quote(self.q) + "&from=" + self.from_ + "&to=" + self.to_ + "&appid=" + self.appid + "&salt=" + self.salt + "&sign=" + self.sign
    
    def getHTMLText(self, url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()# 分析返回码，给出异常提示
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return '产生异常'
    
    def get_json_data(self, html):
        translate_text = ''
        result = json.loads(html)
        try:
            result = result['trans_result']
            for item in result:
                translate_text += item['dst']
        except:
            return "False"
        return translate_text 

    def translate(self):
        html_text = self.getHTMLText(self.full_url)
        result = self.get_json_data(html_text)
        return result
