# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:26:35 2018

@author: sr
"""
import hashlib
import requests
import json
import difflib

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


if __name__ == '__main__':
    # print(BaiduTranslate('你的“盐”值爆表了吗？教你“限盐妙招” TITLE CONTENT 秋风起，冬天也渐渐走近，高血压患者也开始担忧血压不稳、心血管病发作。 国际著名期刊“柳叶刀”今年发布研究显示，在中国，饮食结构造成的心血管疾病死亡率在世界人口前20的大国中“喜登“第一，而在所有的饮食风险因素中，影响最大的就是高盐。2018140653。同德医检通。2018140653。你的“盐”值爆表了吗？ 教你“限盐妙招”').translate())
    print(difflib.SequenceMatcher(None, "高血压的罪魁祸首不是盐！而是它，该忌口了！", "【医生说】心血管疾病的预防需要注意这些事项！").quick_ratio())
