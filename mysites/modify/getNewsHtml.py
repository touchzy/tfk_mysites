# -*- coding: utf-8 -*-

import time
import os
import json
import copy

def get_path(path):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)

def zte(str_):
    if str_ == '提倡':
        return 'advocate'
    elif str_ == '反对':
        return 'against'
    elif str_ == '中立':
        return 'neutrality'
    elif str_ == '食物中的钠':
        return 'sodium in food'
    elif str_ == '高血压':
        return 'hypertension'
    elif str_ == '心血管健康':
        return 'cardiovascular health'
    elif str_ == '综合健康信息':
        return 'comprehensive health information'
    elif str_ == '决心工程':
        return 'Resolve To Save Lives'
    elif str_ == '政府':
        return 'government'
    elif str_ == '企业':
        return 'industry'
    elif str_ == '公众' or str_ == '民众':
        return 'public'
    elif str_ == '反式脂肪酸':
        return 'trans fat'

def get_articles(temp, item_list, index, news_index):
    temp = temp.replace("#news_index#", str(news_index))
    temp = temp.replace("#url#", item_list[index].url).replace("#title#", item_list[index].title).replace("#source#", item_list[index].source)
    temp = temp.replace("#news_subject#", item_list[index].news_subject).replace("#attitude#", item_list[index].attitude)
    temp = temp.replace("#time#", item_list[index].time.split("日")[-1])
    temp = temp.replace("#title_en#", item_list[index].title_en).replace("#source_en#", item_list[index].source_en)
    temp = temp.replace("#news_subject_en#", zte(item_list[index].news_subject)).replace("#attitude_en#", zte(item_list[index].attitude))
    temp = temp.replace("#abstract_cn#", item_list[index].abstract_cn).replace("#abstract_en#", item_list[index].abstract_en)
    return temp

def get_content_type(type_list, tag, report_layout, item_list, news_not_found, news_article_layout):
    if not type_list:
        return report_layout.replace(tag, news_not_found)
    else:
        news_index = 0
        temp = ""
        for index in type_list:
            news_index += 1
            temp += get_articles(copy.deepcopy(news_article_layout), item_list, index, news_index)
        return report_layout.replace(tag, temp)

def get_html_content(df_salt, df_fat, date):
    news_article_layout = open(get_path("layout/news_article_layout.html"), "r", encoding="utf8").read()
    news_not_found = open(get_path("layout/news_not_found.html"), "r", encoding="utf8").read()
    news_salt_report_layout = open(get_path("layout/news_salt_report_layout.html"), "r", encoding="utf8").read()
    news_fat_report_layout = open(get_path("layout/news_fat_report_layout.html"), "r", encoding="utf8").read()
    ################减盐###############
    salt_swzdn = []  # 食物中的钠
    salt_gxy = []  # 高血压
    salt_xxgjk = []  # 心血管健康
    salt_jkzx = []  # 健康中心
    salt_jxgc = []  # 决心工程

    salt_swzdn1 = []  # 食物中的钠
    salt_gxy1 = []  # 高血压
    salt_xxgjk1 = []  # 心血管健康
    salt_jkzx1 = []  # 健康中心
    salt_jxgc1 = []  # 决心工程

    salt_swzdn2 = []  # 食物中的钠
    salt_gxy2 = []  # 高血压
    salt_xxgjk2 = []  # 心血管健康
    salt_jkzx2 = []  # 健康中心
    salt_jxgc2 = []  # 决心工程

    salt_swzdn3 = []  # 食物中的钠
    salt_gxy3 = []  # 高血压
    salt_xxgjk3 = []  # 心血管健康
    salt_jkzx3 = []  # 健康中心
    salt_jxgc3 = []  # 决心工程

    salt_swzdn4 = []  # 食物中的钠
    salt_gxy4 = []  # 高血压
    salt_xxgjk4 = []  # 心血管健康
    salt_jkzx4 = []  # 健康中心
    salt_jxgc4 = []  # 决心工程

    salt_zf = []  # 政府
    salt_qy = []  # 企业
    salt_gz = []  # 公众

    ad_1 = 0
    ad_2 = 0
    ad_3 = 0
    ag_1 = 0
    ag_2 = 0
    ag_3 = 0
    ne_1 = 0
    ne_2 = 0
    ne_3 = 0
    
    # 按新闻主体分类
    for index in range(len(df_salt)):
        if df_salt[index].news_subject == "政府":
            salt_zf.append(index)
            if df_salt[index].attitude == "提倡":
                ad_1 += 1
            elif df_salt[index].attitude == "反对":
                ag_1 += 1
            else:
                ne_1 += 1
        elif df_salt[index].news_subject == "企业":
            salt_qy.append(index)
            if df_salt[index].attitude == "提倡":
                ad_2 += 1
            elif df_salt[index].attitude == "反对":
                ag_2 += 1
            else:
                ne_2 += 1
        elif df_salt[index].news_subject == "公众" or df_salt[index].news_subject == "民众":
            salt_gz.append(index)
            if df_salt[index].attitude == "提倡":
                ad_3 += 1
            elif df_salt[index].attitude == "反对":
                ag_3 += 1
            else:
                ne_3 += 1

    # 按内容分类
    for index in range(len(df_salt)):
        if df_salt[index].content_type == "食物中的钠":
            if df_salt[index].province == "山东":
                salt_swzdn.append(index)
            elif df_salt[index].province == "河南":
                salt_swzdn1.append(index)
            elif df_salt[index].province == "安徽":
                salt_swzdn2.append(index)
            elif df_salt[index].province == "浙江":
                salt_swzdn3.append(index)
            else:
                salt_swzdn4.append(index)
        elif df_salt[index].content_type == "高血压":
            if df_salt[index].province == "山东":
                salt_gxy.append(index)
            elif df_salt[index].province == "河南":
                salt_gxy1.append(index)
            elif df_salt[index].province == "安徽":
                salt_gxy2.append(index)
            elif df_salt[index].province == "浙江":
                salt_gxy3.append(index)
            else:
                salt_gxy4.append(index)
        elif df_salt[index].content_type == "心血管健康":
            if df_salt[index].province == "山东":
                salt_xxgjk.append(index)
            elif df_salt[index].province == "河南":
                salt_xxgjk1.append(index)
            elif df_salt[index].province == "安徽":
                salt_xxgjk2.append(index)
            elif df_salt[index].province == "浙江":
                salt_xxgjk3.append(index)
            else:
                salt_xxgjk4.append(index)
        elif df_salt[index].content_type == "决心工程":
            if df_salt[index].province == "山东":
                salt_jxgc.append(index)
            elif df_salt[index].province == "河南":
                salt_jxgc1.append(index)
            elif df_salt[index].province == "安徽":
                salt_jxgc2.append(index)
            elif df_salt[index].province == "浙江":
                salt_jxgc3.append(index)
            else:
                salt_jxgc4.append(index)
        elif df_salt[index].content_type == "综合健康信息":
            if df_salt[index].province == "山东":
                salt_jkzx.append(index)
            elif df_salt[index].province == "河南":
                salt_jkzx1.append(index)
            elif df_salt[index].province == "安徽":
                salt_jkzx2.append(index)
            elif df_salt[index].province == "浙江":
                salt_jkzx3.append(index)
            else:
                salt_jkzx4.append(index)

    news_salt_report_layout = news_salt_report_layout.replace("#ad_list#", json.dumps([ad_1, ad_2, ad_3])).replace("#ag_list#", json.dumps([ag_1, ag_2, ag_3])).replace("#ne_list#", json.dumps([ne_1, ne_2, ne_3]))
    news_salt_report_layout = news_salt_report_layout.replace("#date#", date).replace("#news_num#", str(len(df_salt)))

    #山东
    news_salt_report_layout = get_content_type(salt_swzdn, "#articles_shandong_swzdn#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_gxy, "#articles_shandong_gxy#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_xxgjk, "#articles_shandong_xxgjk#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jkzx, "#articles_shandong_jkzx#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jxgc, "#articles_shandong_jxgc#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)

    #河南
    news_salt_report_layout = get_content_type(salt_swzdn1, "#articles_henan_swzdn#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_gxy1, "#articles_henan_gxy#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_xxgjk1, "#articles_henan_xxgjk#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jkzx1, "#articles_henan_jkzx#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jxgc1, "#articles_henan_jxgc#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)

    # 安徽
    news_salt_report_layout = get_content_type(salt_swzdn2, "#articles_anhui_swzdn#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_gxy2, "#articles_anhui_gxy#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_xxgjk2, "#articles_anhui_xxgjk#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jkzx2, "#articles_anhui_jkzx#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jxgc2, "#articles_anhui_jxgc#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)

    # 浙江
    news_salt_report_layout = get_content_type(salt_swzdn3, "#articles_zhejiang_swzdn#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_gxy3, "#articles_zhejiang_gxy#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_xxgjk3, "#articles_zhejiang_xxgjk#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jkzx3, "#articles_zhejiang_jkzx#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jxgc3, "#articles_zhejiang_jxgc#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)

    # 其他
    news_salt_report_layout = get_content_type(salt_swzdn4, "#articles_other_swzdn#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_gxy4, "#articles_other_gxy#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_xxgjk4, "#articles_other_xxgjk#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jkzx4, "#articles_other_jkzx#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)
    news_salt_report_layout = get_content_type(salt_jxgc4, "#articles_other_jxgc#", news_salt_report_layout, df_salt, news_not_found, news_article_layout)

    ################反式脂肪酸###############
    fat_fszfs = []  # 反式脂肪酸
    fat_jxgc = []  # 决心工程

    fat_fszfs1 = []  # 反式脂肪酸
    fat_jxgc1 = []  # 决心工程

    fat_fszfs2 = []  # 反式脂肪酸
    fat_jxgc2 = []  # 决心工程

    fat_fszfs3 = []  # 反式脂肪酸
    fat_jxgc3 = []  # 决心工程

    fat_fszfs4 = []  # 反式脂肪酸
    fat_jxgc4 = []  # 决心工程

    fat_zf = []  # 政府
    fat_qy = []  # 企业
    fat_gz = []  # 公众

    ad_1 = 0
    ad_2 = 0
    ad_3 = 0
    ag_1 = 0
    ag_2 = 0
    ag_3 = 0
    ne_1 = 0
    ne_2 = 0
    ne_3 = 0

    # 基于新闻主体的分类
    for index in range(len(df_fat)):
        if df_fat[index].news_subject == "政府":
            fat_zf.append(index)
            if df_fat[index].attitude == "提倡":
                ad_1 += 1
            elif df_fat[index].attitude == "反对":
                ag_1 += 1
            else:
                ne_1 += 1
        elif df_fat[index].news_subject == "企业":
            fat_qy.append(index)
            if df_fat[index].attitude == "提倡":
                ad_2 += 1
            elif df_fat[index].attitude == "反对":
                ag_2 += 1
            else:
                ne_2 += 1
        elif df_fat[index].news_subject == "公众" or df_fat[index].news_subject == "民众":
            fat_gz.append(index)
            if df_fat[index].attitude == "提倡":
                ad_3 += 1
            elif df_fat[index].attitude == "反对":
                ag_3 += 1
            else:
                ne_3 += 1
    # 按内容分类
    for index in range(len(df_fat)):
        if df_fat[index].content_type == "反式脂肪酸":
            if df_fat[index].province == "山东":
                fat_fszfs.append(index)
            elif df_fat[index].province == "河南":
                fat_fszfs1.append(index)
            elif df_fat[index].province == "安徽":
                fat_fszfs2.append(index)
            elif df_fat[index].province == "浙江":
                fat_fszfs3.append(index)
            else:
                fat_fszfs4.append(index)
        elif df_fat[index].content_type == "决心工程":
            if df_fat[index].province == "山东":
                fat_jxgc.append(index)
            elif df_fat[index].province == "河南":
                fat_jxgc1.append(index)
            elif df_fat[index].province == "安徽":
                fat_jxgc2.append(index)
            elif df_fat[index].province == "浙江":
                fat_jxgc3.append(index)
            else:
                fat_jxgc4.append(index)

    news_fat_report_layout = news_fat_report_layout.replace("#ad_list#", json.dumps([ad_1, ad_2, ad_3])).replace("#ag_list#", json.dumps([ag_1, ag_2, ag_3])).replace("#ne_list#", json.dumps([ne_1, ne_2, ne_3]))
    news_fat_report_layout = news_fat_report_layout.replace("#date#", date).replace("#news_num#", str(len(df_fat)))

    # 山东
    news_fat_report_layout = get_content_type(fat_fszfs, "#articles_shandong_fszfs#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)
    news_fat_report_layout = get_content_type(fat_jxgc, "#articles_shandong_jxgc#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)

    # 河南
    news_fat_report_layout = get_content_type(fat_fszfs1, "#articles_henan_fszfs#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)
    news_fat_report_layout = get_content_type(fat_jxgc1, "#articles_henan_jxgc#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)

    # 安徽
    news_fat_report_layout = get_content_type(fat_fszfs2, "#articles_anhui_fszfs#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)
    news_fat_report_layout = get_content_type(fat_jxgc2, "#articles_anhui_jxgc#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)

    # 浙江
    news_fat_report_layout = get_content_type(fat_fszfs3, "#articles_zhejiang_fszfs#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)
    news_fat_report_layout = get_content_type(fat_jxgc3, "#articles_zhejiang_jxgc#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)

    # 其他
    news_fat_report_layout = get_content_type(fat_fszfs4, "#articles_other_fszfs#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)
    news_fat_report_layout = get_content_type(fat_jxgc4, "#articles_other_jxgc#", news_fat_report_layout, df_fat, news_not_found, news_article_layout)

    return news_salt_report_layout, news_fat_report_layout
