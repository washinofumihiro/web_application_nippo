# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from .models import Question, AnswerQuestion
from .forms import AnswerForm


def list(question_id):
    answer = Question.objects.all().prefetch_related("answers").get(id=question_id).answers.all()
    # print(answer.question_content)
    return answer


# def show(question_id):
#     if question_id:   # report_id が指定されている (修正時)
#         # question = get_object_or_404(Question, pk=report_id)
#         answer = AnswerQuestion.objects.all().prefetch_related("answers").get(id=question_id).answers.all()[0]
#         # question = Question.abjects.get(id=report_id)
#         # print(question.question_level_1)
#     else:         # report_id が指定されていない (追加時)
#         answer = AnswerQuestion()
#
#     return answer
def show(answer_id):
    if answer_id:   # report_id が指定されている (修正時)
        # question = get_object_or_404(Question, pk=report_id)
        # answer = AnswerQuestion.objects.all().prefetch_related("answers").get(id=question_id).answers.all()[0]
        answer = get_object_or_404(AnswerQuestion, pk=answer_id)
        # question = Question.abjects.get(id=report_id)
        # print(question.question_level_1)
    else:         # report_id が指定されていない (追加時)
        answer = AnswerQuestion()

    return answer


def edit(post_data, answer, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(post_data, instance=answer)  # POST された request データからフォームを作成
    if form.is_valid():  # フォームのバリデーション
        answer = form.save(commit=False)
        answer.question = question
        answer.save()
    return form
