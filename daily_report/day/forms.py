from django.forms import ModelForm
from .models import Book, Impression


class ImpressionForm(ModelForm):
    """感想のフォーム"""
    class Meta:
        model = Impression
        fields = ('comment', )

class BookForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Book
        # fields = ('name', 'publisher', )
        fields = ( 'user','title', 'content',)
        # fields = ('date', 'title', 'user',)

