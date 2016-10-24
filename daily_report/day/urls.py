# -*- coding: utf-8 -*-
from django.conf.urls import url
from day import views


urlpatterns = [
    # 書籍
    url(r'^report/$', views.list_report, name='list_report'),
    url(r'^report/search/$', views.search_report, name='search_report'),
    url(r'^report/creation/$', views.edit_report, name='create_report'),
    url(r'^report/edition/(?P<report_id>\d+)/$',
        views.edit_report, name='edit_report'),
    url(r'^report/delete/(?P<report_id>\d+)/$',
        views.delete_report, name='delete_report'),
    url(r'^report/browse/(?P<report_id>\d+)/$',
        views.browse_report, name='browse_report'),
    url(r'^comment/(?P<report_id>\d+)/$',
        views.list_comment, name='list_comment'),
    url(r'^comment/creation/(?P<report_id>\d+)/$',
        views.edit_comment, name='create_comment'),
    url(r'^comment/edition/(?P<report_id>\d+)/(?P<comment_id>\d+)/$',
        views.edit_comment, name='edit_comment'),
    url(r'^comment/delete/(?P<report_id>\d+)/(?P<comment_id>\d+)/$',
        views.delete_comment, name='delete_comment'),
    url(r'^report/answer/(?P<report_id>\d+)/(?P<question_id>\d+)/$',
        views.list_answer, name='list_answer'),
    url(r'^report/answer/creation/(?P<report_id>\d+)/(?P<question_id>\d+)/$',
        views.edit_answer, name='create_answer'),
    url(r'^report/answer/edition/(?P<report_id>\d+)/(?P<question_id>\d+)/'
        r'(?P<answer_id>\d+)/$', views.edit_answer, name='edit_answer'),
    url(r'^report/question/$', views.list_all_question, name='all_question'),
]
