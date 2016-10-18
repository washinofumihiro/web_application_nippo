# -*- coding: utf-8 -*-
from django.db import models


class Report(models.Model):
    """書籍"""
    title = models.CharField('タイトル', max_length=255)
    content_Y = models.TextField('やったこと(Y)', blank=True)
    content_W = models.TextField('わかったこと(W)', blank=True)
    content_T = models.TextField('次にすること(T)', blank=True)
    user = models.CharField('投稿者', max_length=255)
    user_post_time = models.CharField('投稿時間', max_length=255)
    post_time = models.DateTimeField('投稿時間', auto_now=True)
    create_time = models.DateTimeField('作成時間', auto_now_add=True)

    def __str__(self):
        return self.name


class Impression(models.Model):
    report = models.ForeignKey(Report, verbose_name='日報', related_name='impressions')
    comment = models.TextField('コメント', blank=True)
    comment_user = models.CharField('コメント投稿者', max_length=255)
    comment_time = models.CharField('コメント時間', max_length=255)

    def __str__(self):
        return self.comment


# class QuestionLevel(models.Model):
#     report = models.ForeignKey(Report, verbose_name='日報', related_name='levels')
#     question_level_1 = models.TextField('レベル1', blank=True)
#     question_level_2 = models.TextField('レベル2', blank=True)
#     question_level_3 = models.TextField('レベル3', blank=True)
#     question_level_4 = models.TextField('レベル4', blank=True)
#     question_level_5 = models.TextField('レベル5', blank=True)
#
#     def __str__(self):
#         return self.level


class Question(models.Model):
    report = models.ForeignKey(Report, verbose_name='日報', related_name='questions')
    question_content = models.TextField('質問内容', blank=True)

    def __str__(self):
        return self.question


class AnswerQuestion(models.Model):
    question = models.ForeignKey(Question, verbose_name='質問', related_name='answers')
    answer = models.TextField('質問に対しての回答', blank=True)

    def __str__(self):
        return self.answer
