# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
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

