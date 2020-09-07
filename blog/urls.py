#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-8-28 16:13
# @Author  : lzh
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index),
    path('get_all', views.get_all),
    path('get_all_category', views.get_all_category),
    path('get_tui_by_count', views.get_tui_by_count),
    path('get_new_article', views.get_new_article),
    path('get_hot_article', views.get_hot_article),
    path('get_all_tag', views.get_all_tag),
    path('get_all_link', views.get_all_link),
    path('get_banner', views.get_banner),
    path('get_article', views.get_article),
    path('get_detail', views.get_detail),
]