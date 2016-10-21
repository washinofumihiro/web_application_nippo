# -*- coding: utf-8 -*-
from django.db import models


class Report(models.Model):
    """日報のモデル"""
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


class Comment(models.Model):
    """コメントのモデル"""
    report = models.ForeignKey(Report, verbose_name='日報', related_name='comments')
    comment = models.TextField('コメント', blank=True)
    comment_user = models.CharField('コメント投稿者', max_length=255)
    comment_time = models.CharField('コメント時間', max_length=255)

    def __str__(self):
        return self.comment


class Question(models.Model):
    """質問のモデル"""
    report = models.ForeignKey(Report, verbose_name='日報', related_name='questions')
    question_content = models.TextField('質問内容', blank=True)

    def __str__(self):
        return self.question


class AnswerQuestion(models.Model):
    """質問に対しての回答のフォーム"""
    question = models.ForeignKey(Question, verbose_name='質問', related_name='answers')
    answer = models.TextField('質問に対しての回答', blank=True)

    def __str__(self):
        return self.answer
