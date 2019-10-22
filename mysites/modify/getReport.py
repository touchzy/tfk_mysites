import os
import copy


def get_path(path):
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, path)


def dailyreport(report, date):
    daily_report_layout = open(get_path("layout/daily_report_layout.html"), "r", encoding="utf8").read()
    daily_report_layout = daily_report_layout.replace("#date_monited#", date)
    daily_report_layout = daily_report_layout.replace("#salt_news_report#", report.salt_news_report)
    daily_report_layout = daily_report_layout.replace("#salt_wechat_report#", report.salt_wechat_report)
    daily_report_layout = daily_report_layout.replace("#salt_weibo_report#", report.salt_weibo_report)
    daily_report_layout = daily_report_layout.replace("#fat_news_report#", report.fat_news_report)
    daily_report_layout = daily_report_layout.replace("#fat_wechat_report#", report.fat_wechat_report)
    daily_report_layout = daily_report_layout.replace("#fat_weibo_report#", report.fat_weibo_report)

    return daily_report_layout
