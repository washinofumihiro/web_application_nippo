# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import Report, Question, AnswerQuestion
from ..forms import QuestionForm


def listup(report_id):
    """
    質問一覧を表示
    :param report_id:
    :return:
    """
    comment = Report.objects.all().prefetch_related("impressions")\
        .get(id=report_id).impressions.all()
    return comment


def select(report_id):
    """
    編集または表示する質問を選択
    :param report_id:
    :return:
    """
    if report_id:   # report_id が指定されている (修正時)
        question = Report.objects.all().prefetch_related("questions")\
            .get(id=report_id).questions.all()[0]
    else:         # report_id が指定されていない (追加時)
        question = Question()

    return question


def edit(post_data, question, report_id):
    """
    質問の編集
    :param post_data:
    :param question:
    :param report_id:
    :return:
    """
    report = get_object_or_404(Report, pk=report_id)
    form = QuestionForm(post_data, instance=question)
    if form.is_valid():
        question = form.save(commit=False)
        question.report = report
        question.save()
    return form


def listup_all():
    """
    回答が返ってきていない質問の一覧を表示
    :return:
    """
    question = Question.objects.all()
    question_id_all = question.values('id')
    query_list = []

    # 回答が返ってきていない質問のidを取り出す
    for question_id in question_id_all:
        count_answer = AnswerQuestion.objects\
            .filter(question_id=question_id['id']).count()

        if count_answer == 0:
            query_list.append(question_id['id'])

    # 取り出したidを元に回答なしの質問を選択する
    query = Q()
    queries = [Q(id=word) for word in query_list]
    for item in queries:
        query |= item

    question = Question.objects.filter(query).order_by('id')

    return question
