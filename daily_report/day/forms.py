# from django.forms import ModelForm
from django import forms
from .models import Report, Impression


class ImpressionForm(forms.ModelForm):
    """感想のフォーム"""
    class Meta:
        model = Impression
        fields = ('comment_user', 'comment',)

class ReportForm(forms.ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Report
        # fields = ('name', 'publisher', )
        # fields = ( 'user','title', 'content')
        fields = ( 'user','title', 'content')
        # fields = ( 'user','title', 'content', 'user_login_time', 'user_post_time')
        # fields = ('date', 'title', 'user',)

class SearchForm(forms.Form):

    Search = forms.CharField(max_length=255)
    print('search')
