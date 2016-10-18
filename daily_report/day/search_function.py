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


def select(keyword, target):
    # チェックボックスにチェックがある場合はキーワードから各カラムを検索
    query = Q()
    for data in target:
        if data == 'post_time':
            queries = [Q(post_time__icontains=word) for word in keyword]
            for item in queries:
                query |= item

        elif data == 'user':
            queries = [Q(user__icontains=word) for word in keyword]
            for item in queries:
                query |= item

        elif data == 'title':
            queries = [Q(title__icontains=word) for word in keyword]
            for item in queries:
                query |= item

        elif data == 'content':
            queries_Y = [Q(content_Y__icontains=word) for word in keyword]
            queries_W = [Q(content_W__icontains=word) for word in keyword]
            queries_T = [Q(content_T__icontains=word) for word in keyword]
            for item in queries_Y:
                query |= item
            for item in queries_W:
                query |= item
            for item in queries_T:
                query |= item

    reports = Report.objects.filter(query).order_by('id')
    return reports


def all(keyword):    # チェックボックスにチェックがない場合はキーワードからDB内全検索
    queries1 = [Q(post_time__icontains=word) for word in keyword]
    queries2 = [Q(user__icontains=word) for word in keyword]
    queries3 = [Q(title__icontains=word) for word in keyword]
    queries4 = [Q(content_Y__icontains=word) for word in keyword]
    queries5 = [Q(content_W__icontains=word) for word in keyword]
    queries6 = [Q(content_T__icontains=word) for word in keyword]

    query = queries1.pop(0)
    for item in queries1:
        query |= item
    for item in queries2:
        query |= item
    for item in queries3:
        query |= item
    for item in queries4:
        query |= item
    for item in queries5:
        query |= item
    for item in queries6:
        query |= item

    reports = Report.objects.filter(query).order_by('id')

    return reports
