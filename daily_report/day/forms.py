from django.forms import ModelForm
from .models import Report, Impression


class ImpressionForm(ModelForm):
    """感想のフォーム"""
    class Meta:
        model = Impression
        fields = ('comment', )

class ReportForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Report
        # fields = ('name', 'publisher', )
        # fields = ( 'user','title', 'content')
        fields = ( 'user','title', 'content','user_login_time')
        # fields = ( 'user','title', 'content', 'user_login_time', 'user_post_time')
        # fields = ('date', 'title', 'user',)

