# -*- coding: utf-8 -*-
import os
import copy
import json


def get_path(path):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)


def weibo_dailyreport(weibo_articles_salt, weibo_articles_fat, date, counts_dict):
    weibo_content = open(get_path("layout/weibo_content.html"), "r", encoding="utf8").read()
    weibo_report_layout = open(get_path("layout/weibo_report_layout.html"), "r", encoding="utf8").read()
    not_found = open(get_path("layout/not_found.html"), "r", encoding="utf8").read()

    ################减盐###############
    hot_weibos = ""
    who_weibos = ""
    if weibo_articles_salt:
        for weibo in weibo_articles_salt:
            temp = copy.deepcopy(weibo_content)
            temp = temp.replace("#nick_name#", weibo.user_name)
            try:
                temp = temp.replace("#user_location_cn#", weibo.user_province).replace("#user_location_en#", weibo.user_province_en)
            except:
                print(str(weibo._id))
            if not weibo.user_verified:
                user_identity_cn = "无"
                user_identity_en = "None"
            elif weibo.user_verified_type < 1:
                user_identity_cn = "个人"
                user_identity_en = "Person"
            elif weibo.user_verified_type == 1:
                user_identity_cn = "政务"
                user_identity_en = "Official"
            else:
                user_identity_cn = "机构"
                user_identity_en = "Institution"
            temp = temp.replace("#user_identity_cn#", user_identity_cn).replace("#user_identity_en#", user_identity_en)
            temp = temp.replace("#created_time#", weibo.date + " " + weibo.time)
            temp = temp.replace("#source_cn#", weibo.source).replace("#source_en#", weibo.source)
            temp = temp.replace("#repost_num#", str(weibo.repost)).replace("#comment_num#", str(weibo.comment)).replace("#like_num#", str(weibo.like))
            temp = temp.replace("#content_cn#", weibo.content).replace("#content_en#", weibo.content_en)
            temp = temp.replace("#weibo_id#", weibo._id.split("_")[0])
            if weibo.user_name == '世界卫生组织':
                who_weibos += temp
            else:
                hot_weibos += temp

    if not hot_weibos:
        hot_weibos += not_found
    if not who_weibos:
        who_weibos += not_found

    salt_weibo_report = copy.deepcopy(weibo_report_layout)
    salt_weibo_report = salt_weibo_report.replace("#title_cn#", "减盐").replace("#title_en#", "Salt Reduction")
    salt_weibo_report = salt_weibo_report.replace("#created_date#", date)
    salt_weibo_report = salt_weibo_report.replace("#subject_cn#", "减盐").replace("#subject_en#", "salt reduction").replace("#subject#", "salt")
    salt_weibo_report = salt_weibo_report.replace("#hot_weibo_content#", hot_weibos)
    salt_weibo_report = salt_weibo_report.replace("#who_weibo_content#", who_weibos)
    salt_weibo_report = salt_weibo_report.replace("#date_list#", json.dumps(counts_dict["date_list"]))
    salt_weibo_report = salt_weibo_report.replace("#male_counts#", json.dumps(counts_dict["salt_male_counts"]))
    salt_weibo_report = salt_weibo_report.replace("#female_counts#", json.dumps(counts_dict["salt_female_counts"]))
    salt_weibo_report = salt_weibo_report.replace("#weibo_count#", str(counts_dict["salt_female_counts"][-1] + counts_dict["salt_male_counts"][-1]))

    ################反式脂肪酸###############
    hot_weibos = ""
    who_weibos = ""
    if weibo_articles_fat:
        for weibo in weibo_articles_fat:
            temp = copy.deepcopy(weibo_content)
            temp = temp.replace("#nick_name#", weibo.user_name)
            temp = temp.replace("#user_location_cn#", weibo.user_province).replace("#user_location_en#", weibo.user_province_en)
            if not weibo.user_verified:
                user_identity_cn = "无"
                user_identity_en = "None"
            elif weibo.user_verified_type < 1:
                user_identity_cn = "个人"
                user_identity_en = "Person"
            elif weibo.user_verified_type == 1:
                user_identity_cn = "政务"
                user_identity_en = "Official"
            else:
                user_identity_cn = "机构"
                user_identity_en = "Institution"
            temp = temp.replace("#user_identity_cn#", user_identity_cn).replace("#user_identity_en#", user_identity_en)
            temp = temp.replace("#created_time#", weibo.date + " " + weibo.time)
            temp = temp.replace("#source_cn#", weibo.source).replace("#source_en#", weibo.source)
            temp = temp.replace("#repost_num#", str(weibo.repost)).replace("#comment_num#", str(weibo.comment)).replace("#like_num#", str(weibo.like))
            temp = temp.replace("#content_cn#", weibo.content).replace("#content_en#", weibo.content_en)
            temp = temp.replace("#weibo_id#", weibo._id.split("_")[0])
            if weibo.user_name == '世界卫生组织':
                who_weibos += temp
            else:
                hot_weibos += temp

    if not hot_weibos:
        hot_weibos += not_found
    if not who_weibos:
        who_weibos += not_found

    fat_weibo_report = copy.deepcopy(weibo_report_layout)
    fat_weibo_report = fat_weibo_report.replace("#title_cn#", "反式脂肪酸").replace("#title_en#", "Transfat")
    fat_weibo_report = fat_weibo_report.replace("#created_date#", date)
    fat_weibo_report = fat_weibo_report.replace("#subject_cn#", "反式脂肪酸").replace("#subject_en#", "transfat reduction").replace("#subject#", "transfat")
    fat_weibo_report = fat_weibo_report.replace("#hot_weibo_content#", hot_weibos)
    fat_weibo_report = fat_weibo_report.replace("#who_weibo_content#", who_weibos)
    fat_weibo_report = fat_weibo_report.replace("#date_list#", json.dumps(counts_dict["date_list"]))
    fat_weibo_report = fat_weibo_report.replace("#male_counts#", json.dumps(counts_dict["fat_male_counts"]))
    fat_weibo_report = fat_weibo_report.replace("#female_counts#", json.dumps(counts_dict["fat_female_counts"]))
    fat_weibo_report = fat_weibo_report.replace("#weibo_count#", str(counts_dict["fat_female_counts"][-1] + counts_dict["fat_male_counts"][-1]))

    return salt_weibo_report, fat_weibo_report
