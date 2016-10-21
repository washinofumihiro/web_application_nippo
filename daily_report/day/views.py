# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from . import comment_api
from . import question_answer_api
from . import question_level_api
from . import report_api
from . import search_function
from . import user_config
from .forms import ReportForm, CommentForm, QuestionForm, SearchForm, AnswerForm
from .models import Report, Question


def create_user(request):
    """
    ユーザの作成
    :param request:
    :return:
    """
    if request.method == 'POST':
        # ユーザ作成、エラーがあった場合はエラーメッセージを入れる
        error_message = user_config.create_user(request.POST)
        if error_message:
            return render(request, 'day/register.html', {'error_message': error_message})
        else:
            return redirect('/')
    else:
        return render_to_response('day/register.html', {},
                                  context_instance=RequestContext(request))


@login_required
def report_list(request):
    """
    日報のリストを表示
    :param request:
    :return:
    """
    reports = report_api.listup
    form = SearchForm()
    return render(request,
                  'day/report_list.html',
                  {'reports': reports, 'form': form})


@login_required
def report_edit(request, report_id=None):
    """
    日報と質問の新規追加と編集
    :param request:
    :param report_id:
    :return:
    """
    report = report_api.select(report_id, request.user.username)
    question = question_level_api.select(report_id)

    if request.method == 'POST':
        report_form, report_id = report_api.edit(request.POST, report, request.user.username)
        question_form = question_level_api.edit(request.POST, question, report_id)

        if report_form.is_valid():
            return redirect('day:report_list')
    else:
        report_form = ReportForm(instance=report)
        question_form = QuestionForm(instance=question)

    return render(request, 'day/report_edit.html',
                  {'report_form': report_form, 'question_form': question_form,
                   'report_id': report_id, 'question': question})


@login_required
def report_browse(request, report_id=None):
    """
    日報および質問の表示
    :param request:
    :param report_id:
    :return:
    """
    report = report_api.select(report_id, request.user.username)
    question = question_level_api.select(report_id)

    return render(request, 'day/report_browse.html',
                  dict(report_form=report, question=question, report_id=report_id))


@login_required
def report_del(request, report_id):
    """
    日報の削除
    :param request:
    :param report_id:
    :return:
    """
    report_api.delete(report_id)
    return redirect('day:report_list')


def list_comment(request, report_id=None):
    """
    コメントの表示
    :param request:
    :param report_id:
    :return:
    """
    comment = comment_api.listup(report_id)
    report = get_object_or_404(Report, pk=report_id)
    return render(request,
                  'day/comment_list.html',
                  {'comments': comment, 'report': report, 'report_id': report_id})


@login_required
def comment_edit(request, report_id, comment_id=None):
    """
    コメントの新規追加と編集
    :param request:
    :param report_id:
    :param comment_id:
    :return:
    """
    comment = comment_api.select(comment_id, request.user.username)
    if request.method == 'POST':
        form = comment_api.edit(request.POST, comment, report_id)
        if form.is_valid():
            return redirect('day:comment_list', report_id=report_id)
    else:
        form = CommentForm(instance=comment)

    return render(request,
                  'day/comment_edit.html',
                  dict(form=form, report_id=report_id, comment_id=comment_id))


@login_required
def comment_del(request, report_id, comment_id):
    """
    コメントの削除
    :param request:
    :param report_id:
    :param comment_id:
    :return:
    """
    comment_api.delete(comment_id)
    return redirect('day:comment_list', report_id=report_id)


def list_all_question(request):
    """
    回答のない質問の一覧を表示
    :param request:
    :return:
    """
    question = question_level_api.listup_all()

    return render(request,
                  'day/all_question.html',
                  {'question': question})


def list_answer(request, report_id, question_id=None):
    """
    回答の一覧を表示
    :param request:
    :param report_id:
    :param question_id:
    :return:
    """
    answer = question_answer_api.listup(question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request,
                  'day/list_answer.html',
                  {'answers': answer, 'question': question, 'question_id': question_id, 'report_id': report_id})


@login_required
def edit_answer(request, report_id, question_id, answer_id=None):
    """
    質問の編集
    :param request:
    :param report_id:
    :param question_id:
    :param answer_id:
    :return:
    """
    answer = question_answer_api.select(answer_id)
    if request.method == 'POST':
        form = question_answer_api.edit(request.POST, answer, question_id)
        if form.is_valid():
            return redirect('day:list_answer', question_id=question_id, report_id=report_id)
    else:
        form = AnswerForm(instance=answer)

    return render(request,
                  'day/edit_answer.html',
                  dict(form=form, question_id=question_id, answer_id=answer_id, report_id=report_id))


def report_search(request):
    """
    日報の検索
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            keyword = form.cleaned_data['Search'].split()
            target = request.GET.getlist('search_form')

            # チェックボックスにチェックがある場合はキーワードから各カラムを検索
            if target:
                reports = search_function.select(keyword, target)

            # チェックボックスにチェックがない場合はキーワードからDB内全検索
            else:
                reports = search_function.all(keyword)

            return render(request,
                          'day/report_list.html',
                          {'reports': reports, 'form': form, 'word': request.GET['Search']})

        else:   # 入力がない場合
            reports = Report.objects.all().order_by('id')
            return render(request,
                          'day/report_list.html',
                          {'reports': reports, 'form': form})

    else:  # 検索フォームを押さない場合
        reports = Report.objects.all().order_by('id')
        return render(request,
                      'day/report_list.html',
                      {'reports': reports})
