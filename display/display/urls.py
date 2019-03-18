"""display URL Configuration

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
from django.conf.urls import url
from django.views.static import serve
from directory import views as dir_views

urlpatterns = [
    path('', dir_views.index),
    path('login', dir_views.login),
    path('home', dir_views.login),
    path('index', dir_views.index),
    url(r'daily_report/(?P<path>.*)', serve, {'document_root': '../daily_report/'}),

    path('admin/', admin.site.urls),
]
