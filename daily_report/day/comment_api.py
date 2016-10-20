# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import Report, Impression
from .forms import ImpressionForm
from datetime import datetime


def list(report_id):
    """
    コメント一覧の表示
    :param report_id:
    :return:
    """
    comment = Report.objects.all().prefetch_related("impressions").get(id=report_id).impressions.all()
    return comment


def show(comment_id, login_user):
    """
    編集または表示するコメントを選択
    :param comment_id:
    :param login_user:
    :return:
    """
    if comment_id:   # report_id が指定されている (修正時)
        comment = get_object_or_404(Impression, pk=comment_id)
    else:         # report_id が指定されていない (追加時)
        comment = Impression()
        comment.comment_user = login_user

    return comment


def edit(post_data, comment, report_id):
    """
    コメントの編集
    :param post_data:
    :param comment:
    :param report_id:
    :return:
    """
    date_object = datetime.now()
    report = get_object_or_404(Report, pk=report_id)
    form = ImpressionForm(post_data, instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.report = report
        comment.comment_time = datetime(*date_object.timetuple()[:6])
        comment.save()
    return form


def delete(comment_id):
    """
    コメントの削除
    :param comment_id:
    :return:
    """
    comment = get_object_or_404(Impression, pk=comment_id)
    comment.delete()
