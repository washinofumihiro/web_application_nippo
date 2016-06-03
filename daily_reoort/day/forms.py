from django.forms import ModelForm
from day.models import Book, Impression


class ImpressionForm(ModelForm):
    """感想のフォーム"""
    class Meta:
        model = Impression
        fields = ('comment', )

class BookForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Book
        fields = ('name', 'publisher', )
        # fields = ('name', 'publisher', 'page',)


