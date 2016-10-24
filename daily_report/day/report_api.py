# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Report
from .forms import ReportForm


def listup():
    """
    日報の一覧表示
    :return:
    """
    reports = Report.objects.all().order_by('id')
    return reports


def select(report_id, login_user):
    """
    編集または表示するための日報を選択
    :param report_id:
    :param login_user:
    :return:
    """
    if report_id:   # report_id が指定されている (修正時)
        report = get_object_or_404(Report, pk=report_id)
    else:         # report_id が指定されていない (追加時)
        report = Report()
        report.user = login_user

    return report


def edit(post_data, report, login_user):
    """
    日報の編集
    :param post_data:
    :param report:
    :param login_user:
    :return:
    """
    form = ReportForm(post_data, instance=report)

    if form.is_valid():
        report = form.save(commit=False)
        report.save()

    report_id = report.id
    
    return form, report_id


def delete(report_id):
    """
    日報の削除
    :param report_id:
    :return:
    """
    report = get_object_or_404(Report, pk=report_id)
    report.delete()
