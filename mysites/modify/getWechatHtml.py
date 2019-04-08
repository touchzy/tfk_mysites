# -*- coding: utf-8 -*-
import os
import copy
import json
from urllib.parse import quote

def get_path(path):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)

def wechat_dailyreport(wechat_articles_salt, wechat_articles_fat, date, counts_dict):
    wechat_article_layout = open(get_path("layout/wechat_article_layout.html"), "r", encoding="utf8").read()
    if counts_dict["salt_counts"][-1] == 0 and counts_dict["fat_counts"][-1] == 0:
        wechat_report_layout = open(get_path("layout/wechat_report_layout_null.html"), "r", encoding="utf8").read()
    else:
        wechat_report_layout = open(get_path("layout/wechat_report_layout.html"), "r", encoding="utf8").read()

    ################减盐###############
    index = 1
    articles_top5 = ""
    for wechat in wechat_articles_salt:
        article_content = copy.deepcopy(wechat_article_layout)
        article_content = article_content.replace("#show_index#", str(index))
        title_cn = wechat.title
        article_url = "https://weixin.sogou.com/weixin?type=2&query=" + quote(title_cn)
        article_content = article_content.replace("#article_url#", article_url)
        article_content = article_content.replace("#title_cn#", title_cn)
        article_content = article_content.replace("#repeat_num#", str(wechat.repeat_num))
        article_content = article_content.replace("#the_date#", wechat.post_date)
        article_content = article_content.replace("#title_en#", wechat.title_en)
        article_content = article_content.replace("#abstract_cn#", wechat.abstract_cn)
        article_content = article_content.replace("#abstract_en#", wechat.abstract_en)
        articles_top5 += article_content
        index += 1

    salt_wechat_report = copy.deepcopy(wechat_report_layout)
    salt_wechat_report = salt_wechat_report.replace("#subject_title_cn#", "减盐").replace("#subject_title_en#", "Salt Reduction")
    salt_wechat_report = salt_wechat_report.replace("#the_date#", date)
    salt_wechat_report = salt_wechat_report.replace("#subject_word#", "salt")
    salt_wechat_report = salt_wechat_report.replace("#article_count#", str(counts_dict["salt_counts"][-1]))
    salt_wechat_report = salt_wechat_report.replace("#date_list#", json.dumps(counts_dict["date_list"])).replace("#count_list#", json.dumps(counts_dict["salt_counts"]))
    salt_wechat_report = salt_wechat_report.replace("#wechat_articles#", articles_top5)

    ################反式脂肪酸###############
    index = 1
    articles_top5 = ""
    for wechat in wechat_articles_fat:
        article_content = copy.deepcopy(wechat_article_layout)
        article_content = article_content.replace("#show_index#", str(index))
        title_cn = wechat.title
        article_url = "https://weixin.sogou.com/weixin?type=2&query=" + quote(title_cn)
        article_content = article_content.replace("#article_url#", article_url)
        article_content = article_content.replace("#title_cn#", title_cn)
        article_content = article_content.replace("#repeat_num#", str(wechat.repeat_num))
        article_content = article_content.replace("#the_date#", wechat.post_date)
        article_content = article_content.replace("#title_en#", wechat.title_en)
        article_content = article_content.replace("#abstract_cn#", wechat.abstract_cn)
        article_content = article_content.replace("#abstract_en#", wechat.abstract_en)
        articles_top5 += article_content
        index += 1

    fat_wechat_report = copy.deepcopy(wechat_report_layout)
    fat_wechat_report = fat_wechat_report.replace("#subject_title_cn#", "反式脂肪酸").replace("#subject_title_en#", "Transfat")
    fat_wechat_report = fat_wechat_report.replace("#the_date#", date)
    fat_wechat_report = fat_wechat_report.replace("#subject_word#", "fat")
    fat_wechat_report = fat_wechat_report.replace("#article_count#", str(counts_dict["fat_counts"][-1]))
    fat_wechat_report = fat_wechat_report.replace("#date_list#", json.dumps(counts_dict["date_list"])).replace("#count_list#", json.dumps(counts_dict["fat_counts"]))
    fat_wechat_report = fat_wechat_report.replace("#wechat_articles#", articles_top5)

    return salt_wechat_report, fat_wechat_report
