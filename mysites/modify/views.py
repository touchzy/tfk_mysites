# -*- coding: utf-8 -*-
import os
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr,formataddr
import traceback

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Wechat_articles, Weibo_content, News_articles, Daily_report, Weibo_notes, User_account, Daily_count
from .baiduTranslate import BaiduTranslate
from .getNewsHtml import get_html_content
from .getWeiboHtml import weibo_dailyreport
from .getWechatHtml import wechat_dailyreport
from .getReport import dailyreport
from bson.objectid import ObjectId

fat_keywords = ["反式脂肪酸", "氢化植物油","部分氢化植物油", "氢化脂肪", "部分氢化脂肪", "植物性酥油", "起酥油", "人造牛油", "人造黄油", "人造奶油", "植脂末", "人造脂肪酸"]


def get_date(date, custom_date):
    return custom_date if custom_date else date


def get_path(path):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)


def date_format(date):
    date_list = date.split("-")
    return date_list[0] + "年" + date_list[1] + "月" + date_list[2] + "日"


from functools import wraps


def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login') == '1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login')
    return inner


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User_account.objects(name=username, password=password)
        if user:
            request.session['is_login'] = '1'
            request.session['user_id'] = user[0]._id
            return redirect('/index')
        else:
            return render(request, 'login.html', {"flag": "用户名或密码错误！"})
    return render(request, 'login.html')


@check_login
def index(request):
    user_id = request.session.get('user_id')
    userobj = User_account.objects(_id=ObjectId(user_id))
    if userobj:
        return render(request,'index.html',{"user":userobj[0].name})
    else:
        return render(request,'index.html')


def is_repeat(title_a, title_b):
    if (title_a in title_b) or (title_b in title_a):
        return True
    else:
        return False


def get_repeat_num(query_set):
    wechat_dict = {}
    for article in query_set:
        if not wechat_dict:
            wechat_dict[article.title] = {"id": article._id, "count": 1}
            continue
        is_unique = True
        for key in wechat_dict.keys():
            if is_repeat(key, article.title):
                wechat_dict[key]["count"] += 1
                is_unique = False
                break
        if is_unique:
            wechat_dict[article.title] = {"id": article._id, "count": 1}
    for key in wechat_dict.keys():
        Wechat_articles.objects(_id=wechat_dict[key]["id"]).update(repeat_num=wechat_dict[key]["count"])


@check_login
def get_wechat(request):
    if request.method == "POST":
        date = request.POST.get("date")
        id = request.POST.get("id")
        subject = request.POST.get("subject")
        submit_type = request.POST.get("submit")
        if submit_type == "submit":
            title = request.POST.get("title")
            abstr = request.POST.get("abstr")
            translate_string = abstr.replace("#", "").replace("&", "") + '2018140653。' + title.replace("#", "").replace("&", "")
            translate_list = BaiduTranslate(translate_string).translate().split('2018140653.')
            try:
                abstr_en = translate_list[0]
                title_en = translate_list[1]
            except:
                title_en = BaiduTranslate(title.replace("#", "").replace("&", "")).translate()
                abstr_en = BaiduTranslate(abstr.replace("#", "").replace("&", "")).translate()
            Wechat_articles.objects(_id=id).update(is_useful=True, to_filter=False, to_check=True, abstract_cn=abstr, abstract_en=abstr_en, title_en=title_en)
        else:
            Wechat_articles.objects(_id=id).update(is_useful=False, to_filter=False, to_check=False)
        if Wechat_articles.objects(post_date=date, subject=subject, status="normal", is_useful=True, to_filter=False, to_check=True).count() < 5:
            wechat_article = Wechat_articles.objects(post_date=date, subject=subject, status="normal", to_filter=True).order_by("-repeat_num").limit(1)
            if wechat_article:
                article = wechat_article[0]
                article.id = article._id
                return render(request, "wechat_articles.html", {"article": article, "date": date})
            else:
                if subject == "1":
                    wechat_article = Wechat_articles.objects(post_date=date, subject="2", status="normal", to_filter=True).order_by("-repeat_num").limit(1)
                    if wechat_article:
                        article = wechat_article[0]
                        article.id = article._id
                        return render(request, "wechat_articles.html", {"article": article, "date": date})
                    else:
                        message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
                        return render(request, "message.html", {"message": message})
                else:
                    message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
                    return render(request, "message.html", {"message": message})
        else:
            if subject == "1":
                wechat_article = Wechat_articles.objects(post_date=date, subject="2", status="normal", to_filter=True).order_by("-repeat_num").limit(1)
                if wechat_article:
                    article = wechat_article[0]
                    article.id = article._id
                    return render(request, "wechat_articles.html", {"article": article, "date": date})
                else:
                    message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
                    return render(request, "message.html", {"message": message})
            else:
                message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
                return render(request, "message.html", {"message": message})
    else:
        date = get_date(request.GET.get("date"), request.GET.get("custom_date"))
        if Wechat_articles.objects(post_date=date, is_useful=True).count() == 10:
            message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
            return render(request, "message.html", {"message": message})
        else:
            if Wechat_articles.objects(post_date=date):
                get_repeat_num(Wechat_articles.objects(post_date=date, subject="1", status="normal"))
                get_repeat_num(Wechat_articles.objects(post_date=date, subject="2", status="normal"))
            else:
                message = date_format(date) + '微信无数据！请返回首页重新输入日期'
                return render(request, "message.html", {"message": message})
            if Wechat_articles.objects(post_date=date, subject="1", status="normal", is_useful=True).count() < 5:
                wechat_article = Wechat_articles.objects(post_date=date, subject="1", status="normal", to_filter=True).order_by("-repeat_num").limit(1)
                if wechat_article:
                    article = wechat_article[0]
                    article.id = article._id
                    return render(request, "wechat_articles.html", {"article": article, "date": date})
                else:
                    if Wechat_articles.objects(post_date=date, subject="2", status="normal", is_useful=True).count() < 5:
                        wechat_article = Wechat_articles.objects(post_date=date, subject="2", status="normal", to_filter=True).order_by("-repeat_num").limit(1)
                        if wechat_article:
                            article = wechat_article[0]
                            article.id = article._id
                            return render(request, "wechat_articles.html", {"article": article, "date": date})
                        else:
                            message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
                            return render(request, "message.html", {"message": message})
                    else:
                        message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
                        return render(request, "message.html", {"message": message})
            else:
                wechat_article = Wechat_articles.objects(post_date=date, subject="2", status="normal", to_filter=True).order_by("-repeat_num").limit(1)
                if wechat_article:
                    article = wechat_article[0]
                    article.id = article._id
                    return render(request, "wechat_articles.html", {"article": article, "date": date})
                else:
                    message = date_format(date) + '微信筛选完成！请返回首页继续进行核对工作'
                    return render(request, "message.html", {"message": message})


def get_relation(query_set, date):
    salt_male, salt_female, fat_male, fat_female = 0, 0, 0, 0
    for article in query_set:
        is_related, flag = True, False
        text = article.content + article.ori_content
        for user_name in article.user_list:
            text = text.replace(user_name, " ")
        if ("盐" in "".join(article.user_list) and "盐" not in text) or ("钠" in "".join(article.user_list) and "钠" not in text):
            is_related = False
            flag = True
        filter_keys = ["盐甜", "咸甜", "可甜可盐", "高盐值", "带盐", "盐焗", "美食", "盐“数字”", "调味", "适量盐", " 盐 ", "代盐",
                       "少量的盐", "可盐可甜", "美味", "撒盐", "放点盐", "很盐", "盐汽水", "盐少许", "拌上盐", "放上盐", "竹盐",
                       "盐水沟", "加盐", "盐系", "盐浓度", "盐亦凡", "产盐", "抹盐", "盐少了", "可咸可甜", "一点盐", "点盐", "盐铅",
                       "可盐可", "洗干净", "切成段", "翻炒", "葱末", "炒匀", "切段", "菜谱", "、盐、", "热锅", "爆炒", "，盐，",
                       "盐水", "超级盐", "加入盐", "排骨", "食谱", "米饭", "拌饭", "张艺兴", "洗净", "洗干净", "调味", "炒面", "制盐",
                       "超级盐", "盐粉", "陕西菜", "炒鸡", "炒面", "土豆丝", "做饭", "做饭", "泡椒", "鱿鱼", "腊肠", "杏鲍菇", "金针菇",
                       "鱿鱼", "下单", "淘宝", "禾然", "￥", "豆瓣酱", "贼香", "拌匀", "家乡菜", "鲜美", "盐放少了", "胖盐", "中科盐发",
                       "丑女", "凉拌", "非常盐", "可萌可盐", "酱牛肉", "红烧肉", "盐放多了", "王源", "苏宁", "袋盐", "缺米少盐",
                       "格兰特", "包邮"]
        useful_keys = ["健康", "养生", "长寿", "高血压", "公共卫生", "世界卫生组织", "WHO"]
        if not flag:
            for key in useful_keys:
                if key in text:
                    is_related = True
                    flag = True
                    break
            if not flag:
                for key in filter_keys:
                    if key in text:
                        is_related = False
                        break
        if is_related:
            if article.subject == "盐" and article.user_sex == "男":
                salt_male += 1
            elif article.subject == "盐" and article.user_sex == "女":
                salt_female += 1
            elif article.subject == "反式脂肪酸" and article.user_sex == "男":
                fat_male += 1
            elif article.subject == "反式脂肪酸" and article.user_sex == "女":
                fat_female += 1
        Weibo_content.objects(_id=article._id).update(is_related=is_related)
    new_note = Weibo_notes(_id=date, salt_male=salt_male, salt_female=salt_female, fat_male=fat_male, fat_female=fat_female)
    new_note.save()


@check_login
def get_weibo(request):
    if request.method == "POST":
        date = request.POST.get("date")
        id = request.POST.get("id")
        submit_type = request.POST.get("submit")
        if submit_type == "submit":
            weibo = Weibo_content.objects(_id=id)
            content_en = BaiduTranslate(weibo[0].content.replace("#", "").replace("&", "")).translate()
            user_province_en = BaiduTranslate(weibo[0].user_province).translate()
            weibo.update(is_useful=True, to_filter=False, to_check=True, content_en=content_en, user_province_en=user_province_en)
        else:
            weibo = Weibo_content.objects(_id=id)
            note = Weibo_notes.objects(_id=date)
            if weibo[0].subject == "盐" and weibo[0].user_sex == "男":
                salt_male = note[0].salt_male - 1
                note.update(salt_male=salt_male)
            elif weibo[0].subject == "盐" and weibo[0].user_sex == "女":
                salt_female = note[0].salt_female - 1
                note.update(salt_female=salt_female)
            elif weibo[0].subject == "反式脂肪酸" and weibo[0].user_sex == "男":
                fat_male = note[0].fat_male - 1
                note.update(fat_male=fat_male)
            elif weibo[0].subject == "反式脂肪酸" and weibo[0].user_sex == "女":
                fat_female = note[0].fat_female - 1
                note.update(fat_female=fat_female)
            weibo.update(is_useful=False, to_filter=False, to_check=False, is_related=False)
        weibo_article = Weibo_content.objects(date=date, is_ori=1, repost__gte=50, to_filter=True, is_related=True).limit(1)
        if weibo_article:
            article = weibo_article[0]
            article.id = article._id
            return render(request, "weibo_articles.html", {"article": article, "date": date})
        else:
            message = date_format(date) + '微博筛选完成！请返回首页继续进行核对工作'
            return render(request, "message.html", {"message": message})
    else:
        date = get_date(request.GET.get("date"), request.GET.get("custom_date"))
        if Weibo_content.objects(date=date, is_related__in=[True, False]).count() != Weibo_content.objects(date=date).count():
            if Weibo_content.objects(date=date):
                get_relation(Weibo_content.objects(date=date), date)
            else:
                message = date_format(date) + '微博无数据！请返回首页重新输入日期'
                return render(request, "message.html", {"message": message})
            weibo_article = Weibo_content.objects(date=date, is_ori=1, repost__gte=50, to_filter=True, is_related=True).limit(1)
            if weibo_article:
                article = weibo_article[0]
                article.id = article._id
                return render(request, "weibo_articles.html", {"article": article, "date": date})
            else:
                message = date_format(date) + '微博筛选完成！请返回首页继续进行核对工作'
                return render(request, "message.html", {"message": message})
        else:
            weibo_article = Weibo_content.objects(date=date, is_ori=1, repost__gte=50, to_filter=True, is_related=True).limit(1)
            if weibo_article:
                article = weibo_article[0]
                article.id = article._id
                return render(request, "weibo_articles.html", {"article": article, "date": date})
            else:
                salt_male, salt_female, fat_male, fat_female = 0, 0, 0, 0
                for article in Weibo_content.objects(date=date, is_related=True):
                    if article.subject == "盐" and article.user_sex == "男":
                        salt_male += 1
                    elif article.subject == "盐" and article.user_sex == "女":
                        salt_female += 1
                    elif article.subject == "反式脂肪酸" and article.user_sex == "男":
                        fat_male += 1
                    elif article.subject == "反式脂肪酸" and article.user_sex == "女":
                        fat_female += 1
                new_note = Weibo_notes(_id=date, salt_male=salt_male, salt_female=salt_female, fat_male=fat_male, fat_female=fat_female)
                new_note.save()
                message = date_format(date) + '微博筛选完成！请返回首页继续进行核对工作'
                return render(request, "message.html", {"message": message})


@check_login
def get_news(request):
    if request.method == "POST":
        date = request.POST.get("date")
        id = request.POST.get("id")
        submit_type = request.POST.get("submit")
        if submit_type == "submit":
            news_subject = request.POST.get("news_subject")
            content_type = request.POST.get("content_type")
            attitude = request.POST.get("attitude")
            province = request.POST.get("province")
            abstr = request.POST.get("abstr")
            title = request.POST.get("title")
            source = request.POST.get("source")
            translate_string = abstr.replace("#", "").replace("&", "") + '2018140653。' + source.replace("#", "").replace("&", "") + '。' + '2018140653。' + title.replace("#", "").replace("&", "")
            translate_list = BaiduTranslate(translate_string).translate().split('2018140653.')
            try:
                abstr_en = translate_list[0]
                source_en = translate_list[1].replace('.', '')
                title_en = translate_list[2]
            except:
                abstr_en = BaiduTranslate(abstr.replace("#", "").replace("&", "")).translate()
                title_en = BaiduTranslate(title.replace("#", "").replace("&", "")).translate()
                source_en = BaiduTranslate(source.replace("#", "").replace("&", "")).translate()
            try:
                new = News_articles.objects(_id=ObjectId(id))
                if new:
                    new.update(is_useful=True, to_filter=False, to_check=True, news_subject=news_subject,
                               content_type=content_type, attitude=attitude, province=province, abstract_cn=abstr, abstract_en=abstr_en, title_en=title_en, source_en=source_en)
                else:
                    News_articles.objects(_id=id).update(is_useful=True, to_filter=False, to_check=True, news_subject=news_subject,
                                                         content_type=content_type, attitude=attitude, province=province, abstract_cn=abstr, abstract_en=abstr_en, title_en=title_en, source_en=source_en)
            except:
                News_articles.objects(_id=id).update(is_useful=True, to_filter=False, to_check=True, news_subject=news_subject,
                                                     content_type=content_type, attitude=attitude, province=province, abstract_cn=abstr, abstract_en=abstr_en, title_en=title_en, source_en=source_en)
        else:
            try:
                new = News_articles.objects(_id=ObjectId(id))
                if new:
                    new.update(is_useful=False, to_filter=False, to_check=False)
                else:
                    News_articles.objects(_id=id).update(is_useful=False, to_filter=False, to_check=False)
            except:
                News_articles.objects(_id=id).update(is_useful=False, to_filter=False, to_check=False)
        remain = News_articles.objects(time__contains=date, to_filter=True).count()-1
        news_article = News_articles.objects(time__contains=date, to_filter=True).limit(1)
        if news_article:
            article = news_article[0]
            article.id = article._id
            return render(request, "news_articles.html", {"article": article, "date": date, "remain": remain})
        else:
            message = date + '新闻筛选完成！请返回首页继续进行核对工作'
            return render(request, "message.html", {"message": message})
    else:
        date = date_format(get_date(request.GET.get("date"), request.GET.get("custom_date")))
        if not News_articles.objects(time__contains=date):
            message = date + '新闻无数据！请返回首页重新输入日期'
            return render(request, "message.html", {"message": message})
        else:
            remain = News_articles.objects(time__contains=date, to_filter=True).count()-1
            news_article = News_articles.objects(time__contains=date, to_filter=True).limit(1)
            if news_article:
                article = news_article[0]
                article.id = article._id
                return render(request, "news_articles.html", {"article": article, "date": date, "remain": remain})
            else:
                message = date + '新闻筛选完成！请返回首页继续进行核对工作'
                return render(request, "message.html", {"message": message})


@check_login
def check(request):
    if request.method == "POST":
        date = request.POST.get("date")
        type = request.POST.get("type")
        id = request.POST.get("id")
        if type == "wechat":
            title_en = request.POST.get("title_en")
            abstract_en = request.POST.get("abstr_en")
            Wechat_articles.objects(_id=id).update(to_check=False, title_en=title_en, abstract_en=abstract_en)
            wechat_article = Wechat_articles.objects(post_date=date, to_check=True).limit(1)
            if wechat_article:
                article = wechat_article[0]
                article.id = article._id
                return render(request, "wechat_check.html", {"article": article, "date": date})
            else:
                message = date_format(date) + '微信核对完成！请返回首页生成日报'
                return render(request, "message.html", {"message": message})
        elif type == "weibo":
            content_en = request.POST.get("content_en")
            Weibo_content.objects(_id=id).update(to_check=False, content_en=content_en)
            weibo_article = Weibo_content.objects(date=date, to_check=True).limit(1)
            if weibo_article:
                article = weibo_article[0]
                article.id = article._id
                return render(request, "weibo_check.html", {"article": article, "date": date})
            else:
                message = date_format(date) + '微博核对完成！请返回首页生成日报'
                return render(request, "message.html", {"message": message})
        else:
            title_en = request.POST.get("title_en")
            abstract_en = request.POST.get("abstr_en")
            source_en = request.POST.get("source_en")
            try:
                new = News_articles.objects(_id=ObjectId(id))
                if new:
                    new.update(to_check=False, title_en=title_en, abstract_en=abstract_en, source_en=source_en)
                else:
                    News_articles.objects(_id=id).update(to_check=False, title_en=title_en, abstract_en=abstract_en, source_en=source_en)
            except:
                News_articles.objects(_id=id).update(to_check=False, title_en=title_en, abstract_en=abstract_en, source_en=source_en)
            news_article = News_articles.objects(time__contains=date, to_check=True).limit(1)
            if news_article:
                article = news_article[0]
                article.id = article._id
                return render(request, "news_check.html", {"article": article, "date": date})
            else:
                message = date + '新闻核对完成！请返回首页生成日报'
                return render(request, "message.html", {"message": message})
    else:
        date = get_date(request.GET.get("date"), request.GET.get("custom_date"))
        type = request.GET.get("type")
        if type == "wechat":
            wechat_article = Wechat_articles.objects(post_date=date, to_check=True).limit(1)
            if wechat_article:
                article = wechat_article[0]
                article.id = article._id
                return render(request, "wechat_check.html", {"article": article, "date": date})
            else:
                if Wechat_articles.objects(post_date=date):
                    if (Wechat_articles.objects(post_date=date, subject="1", status="normal", is_useful=True).count() < 5 and Wechat_articles.objects(post_date=date, subject="1", status="normal", to_filter=True, repeat_num__ne=None)) or (Wechat_articles.objects(post_date=date, subject="2", status="normal", is_useful=True).count() < 5 and Wechat_articles.objects(post_date=date, subject="2", status="normal", to_filter=True, repeat_num__ne=None)) or not Wechat_articles.objects(post_date=date, status="normal", repeat_num__ne=None):
                        message = date_format(date) + '微信数据未筛选完毕！请等待筛选完毕'
                    else:
                        message = date_format(date) + '微信数据核对完成！请返回首页生成日报'
                else:
                    message = date_format(date) + '微信无数据！请返回首页重新输入日期'
                return render(request, "message.html", {"message": message})
        elif type == "weibo":
            weibo_article = Weibo_content.objects(date=date, to_check=True).limit(1)
            if weibo_article:
                article = weibo_article[0]
                article.id = article._id
                return render(request, "weibo_check.html", {"article": article, "date": date})
            else:
                if Weibo_content.objects(date=date):
                    if Weibo_content.objects(date=date, is_ori=1, repost__gte=50, to_filter=True, is_related=True) or not Weibo_content.objects(date=date, to_filter=True, is_related__in=[True,False]):
                        message = date_format(date) + '微博数据未筛选完毕！请等待筛选完毕'
                    else:
                        message = date + '微博数据核对完成！请返回首页生成日报'
                else:
                    message = date_format(date) + '微博无数据！请返回首页重新输入日期'
                return render(request, "message.html", {"message": message})
        else:
            date = date_format(date)
            news_article = News_articles.objects(time__contains=date, to_check=True).limit(1)
            if news_article:
                article = news_article[0]
                article.id = article._id
                return render(request, "news_check.html", {"article": article, "date": date})
            else:
                if News_articles.objects(time__contains=date):
                    if News_articles.objects(time__contains=date, to_filter=True):
                        message = date + '新闻数据未筛选完毕！请等待筛选完毕'
                    else:
                        message = date + '新闻数据核对完成！请返回首页生成日报'
                else:
                    message = date + '新闻无数据！请返回首页重新输入日期'
                return render(request, "message.html", {"message": message})


def get_counts(date, type):
    date_split = list(map(int, date.split("-")))
    one_day = datetime.timedelta(days=1)
    thirty_days = datetime.timedelta(days=29)
    ed = datetime.date(date_split[0], date_split[1], date_split[2])
    d = ed - thirty_days
    date_list = []
    if type == "weibo":
        salt_male_counts = []
        salt_female_counts = []
        fat_male_counts = []
        fat_female_counts = []
        while d <= ed:
            date_list.append(str(d))
            note = Weibo_notes.objects(_id=str(d))[0]
            salt_male_counts.append(note.salt_male)
            salt_female_counts.append(note.salt_female)
            fat_male_counts.append(note.fat_male)
            fat_female_counts.append(note.fat_female)
            d += one_day
        return {"date_list": date_list, "salt_male_counts": salt_male_counts, "salt_female_counts": salt_female_counts, "fat_male_counts": fat_male_counts, "fat_female_counts": fat_female_counts}
    else:
        salt_counts = []
        fat_counts = []
        daily_counts = Daily_count.objects(_id__gte=str(d))
        for count in daily_counts:
            date_list.append(str(d))
            salt_counts.append(count.wechat_salt_count)
            fat_counts.append(count.wechat_fat_count)
            d += one_day
            if d == ed:
                date_list.append(str(ed))
                if type == "wechat_null":
                    salt_counts.append(0)
                    fat_counts.append(0)
                    break
                salt_counts.append(Wechat_articles.objects(post_date=str(ed), subject="1").count())
                fat_counts.append(Wechat_articles.objects(post_date=str(ed), subject="2").count())
                break
        return {"date_list": date_list, "salt_counts": salt_counts, "fat_counts": fat_counts}


@check_login
def get_html(request):
    date = get_date(request.GET.get("date"), request.GET.get("custom_date"))
    type = request.GET.get("type")
    if type == "wechat":
        if not Wechat_articles.objects(post_date=date):
            message = date_format(date) + '微信暂无数据，无法生成日报。'
            return render(request, "message.html", {"message": message})
        else:
            if Wechat_articles.objects(post_date=date, to_check=True) or not Wechat_articles.objects(post_date=date, is_useful__in=[True, False]):
                message = date_format(date) + '微信仍有工作未完成，无法生成日报。'
                return render(request, "message.html", {"message": message})
            else:
                wechat_articles_salt = Wechat_articles.objects(post_date=date, is_useful=True, subject="1").order_by("-repeat_num")
                wechat_articles_fat = Wechat_articles.objects(post_date=date, is_useful=True, subject="2").order_by("-repeat_num")
                count_dict = get_counts(date, type)
                daily_count = Daily_count.objects(_id=date)
                if daily_count:
                    daily_count.update(wechat_salt_count=count_dict["salt_counts"][-1], wechat_fat_count=count_dict["fat_counts"][-1])
                else:
                    daily_count_new = Daily_count(_id=date, wechat_salt_count=count_dict["salt_counts"][-1], wechat_fat_count=count_dict["fat_counts"][-1])
                    daily_count_new.save()
                salt_wechat_report, fat_wechat_report = wechat_dailyreport(wechat_articles_salt, wechat_articles_fat, date, count_dict)
                daily_report = Daily_report.objects(_id=date)
                if daily_report:
                    daily_report.update(salt_wechat_report=salt_wechat_report, fat_wechat_report=fat_wechat_report)
                else:
                    daily_report_new = Daily_report(_id=date, salt_wechat_report=salt_wechat_report, fat_wechat_report=fat_wechat_report)
                    daily_report_new.save()
                message = date_format(date) + '微信日报生成完毕！'
                return render(request, "message.html", {"message": message})
    elif type == "wechat_null":
        wechat_articles_salt = []
        wechat_articles_fat = []
        count_dict = get_counts(date, type)
        daily_count = Daily_count.objects(_id=date)
        if daily_count:
            daily_count.update(wechat_salt_count=count_dict["salt_counts"][-1], wechat_fat_count=count_dict["fat_counts"][-1])
        else:
            daily_count_new = Daily_count(_id=date, wechat_salt_count=count_dict["salt_counts"][-1], wechat_fat_count=count_dict["fat_counts"][-1])
            daily_count_new.save()
        salt_wechat_report, fat_wechat_report = wechat_dailyreport(wechat_articles_salt, wechat_articles_fat, date, count_dict)
        daily_report = Daily_report.objects(_id=date)
        if daily_report:
            daily_report.update(salt_wechat_report=salt_wechat_report, fat_wechat_report=fat_wechat_report)
        else:
            daily_report_new = Daily_report(_id=date, salt_wechat_report=salt_wechat_report, fat_wechat_report=fat_wechat_report)
            daily_report_new.save()
        message = date_format(date) + '微信日报生成完毕！'
        return render(request, "message.html", {"message": message})
    elif type == "weibo":
        if not Weibo_content.objects(date=date):
            message = date_format(date) + '微博暂无数据，无法生成日报。'
            return render(request, "message.html", {"message": message})
        else:
            if Weibo_content.objects(date=date, to_check=True) or not Weibo_content.objects(date=date, is_related__in=[True, False]):
                message = date_format(date) + '微博仍有工作未完成，无法生成日报。'
                return render(request, "message.html", {"message": message})
            else:
                weibo_articles_salt = Weibo_content.objects(date=date, is_useful=True, subject="盐").order_by("-repost")
                weibo_articles_fat = Weibo_content.objects(date=date, is_useful=True, subject="反式脂肪酸").order_by("-repost")
                count_dict = get_counts(date, type)
                hot_salt = Weibo_content.objects(date=date, is_useful=True, subject="盐").count()
                hot_fat = Weibo_content.objects(date=date, is_useful=True, subject="反式脂肪酸").count()
                daily_count = Daily_count.objects(_id=date)
                if daily_count:
                    daily_count.update(weibo_salt_count=count_dict["salt_male_counts"][-1]+count_dict["salt_female_counts"][-1], weibo_fat_count=count_dict["fat_male_counts"][-1]+count_dict["fat_female_counts"][-1], hot_salt=hot_salt, hot_fat=hot_fat)
                else:
                    daily_count_new = Daily_count(_id=date, weibo_salt_count=count_dict["salt_male_counts"][-1]+count_dict["salt_female_counts"][-1], weibo_fat_count=count_dict["fat_male_counts"][-1]+count_dict["fat_female_counts"][-1], hot_salt=hot_salt, hot_fat=hot_fat)
                    daily_count_new.save()
                salt_weibo_report, fat_weibo_report = weibo_dailyreport(weibo_articles_salt, weibo_articles_fat, date, count_dict)
                daily_report = Daily_report.objects(_id=date)
                if daily_report:
                    daily_report.update(salt_weibo_report=salt_weibo_report, fat_weibo_report=fat_weibo_report)
                else:
                    daily_report_new = Daily_report(_id=date, salt_weibo_report=salt_weibo_report, fat_weibo_report=fat_weibo_report)
                    daily_report_new.save()
                message = date_format(date) + '微博日报生成完毕！'
                return render(request, "message.html", {"message": message})
    else:
        date_news = date_format(date)
        if not News_articles.objects(time__contains=date_news):
            message = date_news + '新闻暂无数据，无法生成日报。'
            return render(request, "message.html", {"message": message})
        else:
            if News_articles.objects(time__contains=date_news, to_filter=True) or News_articles.objects(time__contains=date_news, to_check=True):
                message = date_news + '新闻仍有工作未完成，无法生成日报。'
                return render(request, "message.html", {"message": message})
            else:
                news_articles = News_articles.objects(time__contains=date_news, is_useful=True)
                news_articles_salt = []
                news_articles_fat = []
                important_salt, important_fat = 0, 0
                for article in news_articles:
                    if article.keyword in fat_keywords:
                        news_articles_fat.append(article)
                        if article.province != "其他":
                            important_fat += 1
                    else:
                        news_articles_salt.append(article)
                        if article.province != "其他":
                            important_salt += 1
                daily_count = Daily_count.objects(_id=date)
                if daily_count:
                    daily_count.update(news_salt_count=len(news_articles_salt), news_fat_count=len(news_articles_fat), important_salt=important_salt, important_fat=important_fat)
                else:
                    daily_count_new = Daily_count(_id=date, news_salt_count=len(news_articles_salt), news_fat_count=len(news_articles_fat), important_salt=important_salt, important_fat=important_fat)
                    daily_count_new.save()
                format_salt_news, format_fat_news = get_html_content(news_articles_salt, news_articles_fat, date)
                daily_report = Daily_report.objects(_id=date)
                if daily_report:
                    daily_report.update(salt_news_report=format_salt_news, fat_news_report=format_fat_news)
                else:
                    daily_report_new = Daily_report(_id=date, salt_news_report=format_salt_news, fat_news_report=format_fat_news)
                    daily_report_new.save()
                message = date_news + '新闻日报生成完毕！'
                return render(request, "message.html", {"message": message})


@check_login
def get_report(request):
    date = get_date(request.GET.get("date"), request.GET.get("custom_date"))
    daily_report = Daily_report.objects(_id=date)
    if daily_report:
        report = daily_report[0]
        if report.fat_news_report and report.salt_news_report and report.fat_weibo_report and report.salt_weibo_report and report.fat_wechat_report and report.salt_wechat_report:
            daily_report_html = dailyreport(report, date)
            daily_report_html_upload = daily_report_html.replace("../static/echarts.js", ".static/echarts.js")
            with open("../daily_report/Daily_Reports/dailyReport_%s.html" % date.replace("-", ""), 'w', encoding="utf-8") as f:
                f.write(daily_report_html_upload)
            return HttpResponse(daily_report_html)
        else:
            message = date_format(date) + '仍有工作未完成，无法生成日报。'
            return render(request, "message.html", {"message": message})
    else:
        message = date_format(date) + '仍有工作未完成，无法生成日报。'
        return render(request, "message.html", {"message": message})


@check_login
def upload_daily(request):
    pdf = request.FILES.get("upload")
    if ".pdf" in pdf.name:
        if 'Daily' not in pdf.name:
            return render(request, "message.html", {"message": "上传失败，请上传日报文件！"})
        with open("../daily_report/pdf/%s" % pdf.name, 'wb+') as f:
            for chunk in pdf.chunks():
                f.write(chunk)
        return render(request, "message.html", {"message": "上传成功！"})
    else:
        return render(request, "message.html", {"message": "上传失败，请上传.pdf文件！"})


@check_login
def upload_month(request):
    pdf = request.FILES.get("upload")
    if ".pdf" in pdf.name:
        if 'Monthly' not in pdf.name:
            return render(request, "message.html", {"message": "上传失败，请上传月报文件！"})
        with open("../daily_report/Monthly_Reports/%s" % pdf.name, 'wb+') as f:
            for chunk in pdf.chunks():
                f.write(chunk)
        return render(request, "message.html", {"message": "上传成功！"})
    else:
        return render(request, "message.html", {"message": "上传失败，请上传.pdf文件！"})


def get_compare(num):
    if num >= 0:
        if num >= 100:
            return "（较前日显著增加）"
        elif num >= 10:
            return "（较前日有所增加）"
        elif num >= 2:
            return "（较前日略有增加）"
        else:
            return "（与前日基本一致）"
    else:
        if num <= -100:
            return "（较前日显著减少）"
        elif num <= -10:
            return "（较前日有所减少）"
        elif num <= -2:
            return "（较前日略有减少）"
        else:
            return "（与前日基本一致）"


def get_yesterday(date):
    date_split = list(map(int, date.split("-")))
    today = datetime.date(date_split[0], date_split[1], date_split[2])
    one_day = datetime.timedelta(days=1)
    return str(today - one_day)


def get_string(date):
    daily_count_today = Daily_count.objects(_id=date)
    daily_count_yesterday = Daily_count.objects(_id=get_yesterday(date))
    if daily_count_today and daily_count_yesterday:
        count_today = daily_count_today[0]
        count_yesterday = daily_count_yesterday[0]
        if count_today.news_salt_count and (count_today.wechat_salt_count or count_today.wechat_salt_count == 0) and count_today.weibo_salt_count:
            salt_string = '与“减盐”相关的数据：共监测到%d篇新闻%s，其中属于重点监测省份的有%d篇；获取到%d篇微信公众号文章%s；获取到%d条微博%s，其中转发量超过50的有%d条；\r\n' % (count_today.news_salt_count, get_compare(count_today.news_salt_count - count_yesterday.news_salt_count), count_today.important_salt, count_today.wechat_salt_count, get_compare(count_today.wechat_salt_count - count_yesterday.wechat_salt_count), count_today.weibo_salt_count, get_compare(count_today.weibo_salt_count - count_yesterday.weibo_salt_count), count_today.hot_salt)
            fat_string = '与“反式脂肪酸”相关的数据：共监测到%d篇新闻%s，其中属于重点监测省份的有%d篇；获取到%d篇微信公众号文章%s；获取到%d条微博%s，其中转发量超过50的有%d条。' % (count_today.news_fat_count, get_compare(count_today.news_fat_count - count_yesterday.news_fat_count), count_today.important_fat, count_today.wechat_fat_count, get_compare(count_today.wechat_fat_count - count_yesterday.wechat_fat_count), count_today.weibo_fat_count, get_compare(count_today.weibo_fat_count - count_yesterday.weibo_fat_count), count_today.hot_fat)
            return salt_string + fat_string
        else:
            return ""
    else:
        return ""


@check_login
def show_string(request):
    date = request.POST.get("date")
    string = get_string(date)
    if string != "":
        return render(request, "index.html", {"string": string})
    else:
        return render(request, "message.html", {"message": date_format(date) + "工作未完成，无法统计数据"})


@check_login
def send_email(request):
    # date = request.POST.get("date")
    mail_content = request.POST.get("mail_content").split("\r\n")
    if len(mail_content) == 2:
        date = '2018-12-04'
        sender = 'salt_reduction@163.com'
        password = 'mailfortfk2018'
        # receivers = 'XYin@tobaccofreekids.org,kli@tobaccofreekids.org'
        # cc = '2224169954@qq.com,454507717@qq.com,625088429@qq.com'
        receivers = '1299780716@qq.com'
        cc = 'touchzy@126.com'
        message = MIMEMultipart()
        message['From'] = "%s<%s>" % (Header('“减盐”主题网络数据监测团队', 'GB2312'), Header(sender, "ascii"))
        message['To'] = "%s<1299780716@qq.com>"%Header('哈哈','gb2312')
        message['Cc'] = '哈哈<touchzy@126.com>'
        message['Subject'] = Header(date.replace("-", "") + "日报", 'utf-8')
        html = open(get_path("layout/email_layout.html"), "r", encoding="utf-8").read()
        html = html.replace("#date#", date_format(date)[-6:]).replace("#salt#", mail_content[0]).replace("#fat#", mail_content[1])
        message.attach(MIMEText(html, 'html', 'utf-8'))
        try:
            with open("../daily_report/pdf/Daily Report on %s.pdf" % date, 'rb') as pdf:
                att1 = MIMEText(pdf.read(), 'base64', 'utf-8')
                att1["Content-Type"] = 'application/octet-stream'
                att1["Content-Disposition"] = 'attachment; filename="Daily Report on %s.pdf"' % date
                message.attach(att1)

            smtpObj = smtplib.SMTP()
            smtpObj.connect('smtp.163.com', 25)
            smtpObj.login(sender, password)
            smtpObj.sendmail(sender, receivers.split(',') + cc.split(','), message.as_string())
            return render(request, "message.html", {"message": "发送成功！"})
        except smtplib.SMTPException:
            print(traceback.print_exc())
            return render(request, "message.html", {"message": "发送失败！服务器异常"})
        except IOError:
            return render(request, "message.html", {"message": "发送失败！" + date_format(date) + "pdf未生成"})
    else:
        return render(request, "message.html", {"message": "发送失败！邮件内容有误"})
