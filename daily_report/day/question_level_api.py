from django.shortcuts import render, get_object_or_404, redirect
from .models import Report, Impression, Question
from .forms import ReportForm, ImpressionForm, QuestionForm, SearchForm
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


def list(report_id):
    comment = Report.objects.all().prefetch_related("impressions").get(id=report_id).impressions.all()
    return comment


def show(report_id):
    if report_id:   # report_id が指定されている (修正時)
        # question = get_object_or_404(QuestionLevel, pk=report_id)
        question = Report.objects.all().prefetch_related("questions").get(id=report_id).questions.all()[0]
        # question = QuestionLevel.abjects.get(id=report_id)
        # print(question.question_level_1)
    else:         # report_id が指定されていない (追加時)
        question = Question()

    return question


def edit(post_data, question, report_id):
    report = get_object_or_404(Report, pk=report_id)
    form = QuestionForm(post_data, instance=question)  # POST された request データからフォームを作成
    if form.is_valid():  # フォームのバリデーション
        question = form.save(commit=False)
        question.report = report
        question.save()
    return form
