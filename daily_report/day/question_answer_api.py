# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from .models import Question, AnswerQuestion
from .forms import AnswerForm


def listup(question_id):
    """
    質問に対しての回答一覧を表示
    :param question_id:
    :return:
    """
    answer = Question.objects.all().prefetch_related("answers").get(id=question_id).answers.all()
    return answer


def select(answer_id):
    """
    編集または表示するための回答を選択
    :param answer_id:
    :return:
    """
    if answer_id:   # report_id が指定されている (修正時)
        answer = get_object_or_404(AnswerQuestion, pk=answer_id)
    else:         # report_id が指定されていない (追加時)
        answer = AnswerQuestion()

    return answer


def edit(post_data, answer, question_id):
    """
    回答の編集
    :param post_data:
    :param answer:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(post_data, instance=answer)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.save()
    return form
