# -*- coding: utf-8 -*-
from django.conf.urls import url
from day import views


urlpatterns = [
    # 書籍
    url(r'^report/$', views.report_list, name='report_list'),   # 一覧
    url(r'^report/search/$', views.report_search, name='report_search'),   # 検索後の一覧
    url(r'^report/add/$', views.report_edit, name='report_add'),  # 登録
    url(r'^report/mod/(?P<report_id>\d+)/$', views.report_edit, name='report_mod'),  # 修正
    url(r'^report/del/(?P<report_id>\d+)/$', views.report_del, name='report_del'),   # 削除
    url(r'^report/browse/(?P<report_id>\d+)/$', views.report_browse, name='report_browse'),  # 閲覧
    url(r'^impression/(?P<report_id>\d+)/$', views.list_comment, name='impression_list'),  # 一覧
    url(r'^impression/add/(?P<report_id>\d+)/$', views.impression_edit, name='impression_add'),        # 登録
    url(r'^impression/mod/(?P<report_id>\d+)/(?P<impression_id>\d+)/$', views.impression_edit, name='impression_mod'),  # 修正
    url(r'^impression/del/(?P<report_id>\d+)/(?P<impression_id>\d+)/$', views.impression_del, name='impression_del'),
    url(r'^report/answer/(?P<report_id>\d+)/(?P<question_id>\d+)/$', views.list_answer, name='list_answer'),  # 一覧
    url(r'^report/answer/add/(?P<report_id>\d+)/(?P<question_id>\d+)/$', views.edit_answer, name='add_answer'),  # 登録
    url(r'^report/answer/mod/(?P<report_id>\d+)/(?P<question_id>\d+)/(?P<answer_id>\d+)/$', views.edit_answer, name='mod_answer'),
    url(r'^report/question/$', views.list_all_question, name='all_question'),
]
