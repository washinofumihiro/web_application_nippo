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


def create_user(request):
    user_id = request['user_id']
    password = request['password']
    mail_address = request['mail_address']
    error_message = ""
    password_length = 8

    if len(password) < password_length:
        error_message = 'パスワードは8文字以上で設定してください'
        return error_message

    try:
        new_user = User.objects.create_user(user_id, mail_address, password)
        new_user.save()
        return error_message

    except ValueError:
        error_message = 'User IDが空白です。User IDを入力してください。'
        return error_message

    except IntegrityError:
        error_message = 'すでに存在しているUser IDです。別のUser IDに変更してください。'
        return error_message

