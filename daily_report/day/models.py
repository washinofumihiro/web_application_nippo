from django.db import models
from django.contrib.auth.models import User
# from daily_report.daily_report import settings
# from django.contrib.auth import get_user
# from user_auth import settings


#ユーザー情報
# def get_user(request):
#     from django.contrib.auth.models import AnonymousUser
#     try:
#         user_id = request.session[SESSION_KEY]
#         backend_path = request.session[BACKEND_SESSION_KEY]
#         backend = load_backend(backend_path)
#         user = backend.get_user(user_id) or AnonymousUser()
#     except KeyError:
#         user = AnonymousUser()
#     return user



class Book(models.Model):
    """書籍"""
    title = models.CharField('タイトル', max_length=255)
    content = models.TextField('内容', blank=True)
    user = models.CharField('投稿者', max_length=255)

    def __str__(self):
        return self.name


# class Book(models.Model):
#     """書籍"""
#     date = models.CharField('日付', max_length = 20)
#     title = models.CharField('タイトル', max_length=255)
#     contributor = models.CharField('投稿者', max_length=255)
#     #page = models.CharField('投稿者', max_length=255)
#     # publisher = models.CharField('出版社', max_length=255, blank=True)
#     #page = models.IntegerField('ページ', blank=True, default=0)
#     #page = User.username
#     # page = models.IntegerField('ページ数', blank=True, default=0)
#
#     def __str__(self):
#         return self.name



class Impression(models.Model):
    """感想"""
    book = models.ForeignKey(Book, verbose_name='書籍', related_name='impressions')
    comment = models.TextField('コメント', blank=True)

    def __str__(self):
        return self.comment



