# -*- coding:utf-8 -*-
import pandas as pd
from pymongo import MongoClient

host = '114.242.177.193'
port = 27017
conn = MongoClient(host=host, port=port, tz_aware=False)
db = conn.get_database("tfk_project")
db.authenticate('spider_user', 'mongdb_for_tfk@yuquan')
news = db.news_articles

year = "2019"
month = "2"
month_excel = "02"
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]

for day in days:
    data = news.find({'time': {'$regex': '{}年.*{}月.*{}日.*'.format(year, month, day)}, 'is_useful': True})

    dataList_salt = [["内容分类", "新闻主体分类", "省份", "态度标签", "标题", "发表时间",	"来源",	"网址",	"内容", "关键词", "中文摘要", "摘要翻译", "标题翻译", "来源翻译"]]
    dataList_fat = [["内容分类", "新闻主体分类", "省份", "态度标签", "标题", "发表时间", "来源", "网址", "内容", "关键词", "中文摘要", "摘要翻译", "标题翻译", "来源翻译"]]

    for item in data:
        if item['keyword'] in ["反式脂肪酸", "氢化植物油", "部分氢化植物油", "氢化脂肪", "部分氢化脂肪", "植物性酥油", "起酥油", "人造牛油", "人造黄油", "人造奶油", "植脂末", "人造脂肪酸"]:
            dataList_fat.append([item['content_type'], item['news_subject'], item['province'], item['attitude'], item['title'], item['time'], item['source'], item['url'], str(item['content']), item['keyword'], item['abstract_cn'], item['abstract_en'], item['title_en'], item['source_en']])
        else:
            dataList_salt.append([item['content_type'], item['news_subject'], item['province'], item['attitude'], item['title'], item['time'], item['source'], item['url'], str(item['content']), item['keyword'], item['abstract_cn'], item['abstract_en'], item['title_en'], item['source_en']])

    salt = pd.DataFrame(dataList_salt)
    fat = pd.DataFrame(dataList_fat)

    salt.to_excel('excels/news_salt_{}{}{}.xlsx'.format(year, month_excel, day), index=False, encoding='utf8', header=False)
    fat.to_excel('excels/news_fat_{}{}{}.xlsx'.format(year, month_excel, day), index=False, encoding='utf8', header=False)
