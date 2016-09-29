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
from . import user_config
from . import report_api
from . import comment_api
from . import search_function


def create_user(request):
    # POSTかGETか
    if request.method == 'POST':
        # ユーザ作成、エラーがあった場合はエラーメッセージを入れる
        error_message = user_config.create_user(request.POST)
        if error_message:
            return render(request, 'day/register.html', {'error_message': error_message})
        else:
            return redirect('/')
    else:  # GET の時
        return render_to_response('day/register.html', {},
                                  context_instance=RequestContext(request))


@login_required
def report_list(request):
    reports = report_api.list
    form = SearchForm()
    return render(request,
                  'day/report_list.html',     # 使用するテンプレート
                  {'reports': reports, 'form': form})         # テンプレートに渡すデータ


@login_required
def report_edit(request, report_id=None):

    # 日報の選択
    report = report_api.show(report_id, request.user.username)

    # POSTかGETか
    if request.method == 'POST':
        form = report_api.edit(report, request.POST, request.user.username)
        if form.is_valid():
            return redirect('day:report_list')
    else:  # GET の時
        form = ReportForm(instance=report)  # report インスタンスからフォームを作成

    return render(request, 'day/report_edit.html', dict(form=form, report_id=report_id))


@login_required
def report_browse(request, report_id=None):
    """書籍の編集"""
#     return HttpResponse('書籍の編集')
    if report_id:   # report_id が指定されている (修正時)
        report = get_object_or_404(Report, pk=report_id)
    else:         # report_id が指定されていない (追加時)
        report = Report()

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            report = form.save(commit=False)
            report.save()
            return redirect('day:report_list')
    else:    # GET の時
        form = ReportForm(instance=report)  # report インスタンスからフォームを作成

    return render(request, 'day/report_browse.html', dict(form=form, report_id=report_id))


@login_required
def report_del(request, report_id):
    """書籍の削除"""
    report_api.delete(report_id)
    return redirect('day:report_list')


def list_comment(request, report_id=None):
    comment = comment_api.list(report_id)
    report = get_object_or_404(Report, pk=report_id)
    return render(request,
                  'day/impression_list.html',  # 使用するテンプレート
                  {'impressions': comment, 'report': report})


@login_required
def impression_edit(request, report_id, impression_id=None):
    """感想の編集"""
    # コメントが新規か編集かを選択
    comment = comment_api.show(impression_id, request.user.username)
    if request.method == 'POST':
        form = comment_api.edit(request.POST, comment, report_id)
        # form = ImpressionForm(request.POST, instance=comment)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            return redirect('day:impression_list', report_id=report_id)
    else:    # GET の時
        form = ImpressionForm(instance=comment)  # impression インスタンスからフォームを作成

    return render(request,
                  'day/impression_edit.html',
                  dict(form=form, report_id=report_id, impression_id=impression_id))


@login_required
def impression_del(request, report_id, impression_id):
    """感想の削除"""
    comment_api.delete(impression_id)
    return redirect('day:impression_list', report_id=report_id)


# 検索フォームの作成
def report_search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            keyword = form.cleaned_data['Search'].split()
            # チェックボックスにチェックがある場合はキーワードから各カラムを検索
            target = request.GET.getlist('search_form')
            if target:
                reports = search_function.select(keyword, target)

            # チェックボックスにチェックがない場合はキーワードからDB内全検索
            else:
                reports = search_function.all(keyword)

            return render(request,
                          'day/report_list.html',
                          {'reports': reports, 'form': form, 'word': request.GET['Search']})         # テンプレートに渡すデータ

        else:   # 入力がない場合
            reports = Report.objects.all().order_by('id')
            return render(request,
                          'day/report_list.html',
                          {'reports': reports, 'form': form})  # テンプレートに渡すデータ

    else:  # 検索フォームを押さない場合
        reports = Report.objects.all().order_by('id')
        return render(request,
                      'day/report_list.html',
                      {'reports': reports})  # テンプレートに渡すデータ
