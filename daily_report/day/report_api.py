# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Report, Impression
from .forms import ReportForm, ImpressionForm, SearchForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from .forms import RegisterForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.db import IntegrityError


# 日報の一覧表示
def list():
    reports = Report.objects.all().order_by('id')
    # print(reports.title)
    return reports


# 日報のフォーム指定
def show(report_id, login_user):
    if report_id:   # report_id が指定されている (修正時)
        report = get_object_or_404(Report, pk=report_id)
    else:         # report_id が指定されていない (追加時)
        report = Report()
        report.user = login_user

    return report


# 日報の編集
def edit(post_data, report, login_user):
    form = ReportForm(post_data, instance=report)  # POST された request データからフォームを作成
    if form.is_valid():    # フォームのバリデーション
        report = form.save(commit=False)
        report.save()
        report_id = report.id
    # print(form.is_valid)
    return form, report_id


def delete(report_id):
    report = get_object_or_404(Report, pk=report_id)
    report.delete()


# def make(login_user):
#     report = Report()
#     report.user = login_user
#     form = ReportForm(instance=report)  # report インスタンスからフォームを作成
#
#     return form


@login_required
def report_edit(request, report_id=None):
    if report_id:   # report_id が指定されている (修正時)
        report = get_object_or_404(Report, pk=report_id)
        if report.user != request.user.username:
            return render(request, 'day/report_list.html', {'reports': Report.objects.all().order_by('id')})
    else:         # report_id が指定されていない (追加時)
        report = Report()
        report.user = request.user.username

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            report = form.save(commit=False)
            report.save()
            return redirect('day:report_list')
    else:    # GET の時
        form = ReportForm(instance=report)  # report インスタンスからフォームを作成

    return render(request, 'day/report_edit.html', dict(form=form, report_id=report_id))
