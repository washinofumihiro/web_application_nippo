# -*- coding: utf-8 -*-
from django import forms
from .models import Report, Impression, Question, AnswerQuestion


class ImpressionForm(forms.ModelForm):
    """コメントのフォーム"""
    class Meta:
        model = Impression
        fields = ('comment_user', 'comment',)


class ReportForm(forms.ModelForm):
    """日報のフォーム"""
    class Meta:
        model = Report
        fields = ('user', 'title', 'content_Y', 'content_W', 'content_T',)


class QuestionForm(forms.ModelForm):
    """質問のフォーム"""
    class Meta:
        model = Question
        fields = ('question_content',)


class AnswerForm(forms.ModelForm):
    """質問に対しての回答のフォーム"""
    class Meta:
        model = AnswerQuestion
        fields = ('answer',)


class SearchForm(forms.Form):
    """検索のフォーム"""
    Search = forms.CharField(max_length=255)
