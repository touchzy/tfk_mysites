"""mysites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from modify import views as modify_views

urlpatterns = [
    path('', modify_views.index),
    path('login', modify_views.login),
    path('index', modify_views.index),

    path('wechat/', modify_views.get_wechat),
    path('weibo/', modify_views.get_weibo),
    path('news/', modify_views.get_news),

    path('check/', modify_views.check),
    path('html/', modify_views.get_html),
    path('report/', modify_views.get_report),
    path('upload', modify_views.upload),
    path('send', modify_views.send_email),
    path('string', modify_views.show_string),

    path('admin/', admin.site.urls),
]
