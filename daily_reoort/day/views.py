from django.shortcuts import render, get_object_or_404, redirect
from day.models import Book, Impression
from day.forms import BookForm, ImpressionForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType







@login_required
def book_list(request):
    """書籍の一覧"""
#    return HttpResponse('書籍の一覧')
    books = Book.objects.all().order_by('id')
    return render(request,
                  'day/book_list.html',     # 使用するテンプレート
                  {'books': books})         # テンプレートに渡すデータ

# @login_required
# def book_browse(request):
#     """書籍の一覧"""
# #    return HttpResponse('書籍の一覧')
#     books = Book.objects.all().order_by('id')
#     return render(request,
#                   'day/browse.html',     # 使用するテンプレート
#                   {'books': books})         # テンプレートに渡すデータ


@login_required
def book_edit(request, book_id=None):
    """書籍の編集"""
#     return HttpResponse('書籍の編集')
    if book_id:   # book_id が指定されている (修正時)
        book = get_object_or_404(Book, pk=book_id)
    else:         # book_id が指定されていない (追加時)
        book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            book = form.save(commit=False)
            book.save()
            return redirect('day:book_list')
    else:    # GET の時
        form = BookForm(instance=book)  # book インスタンスからフォームを作成

    return render(request, 'day/book_edit.html', dict(form=form, book_id=book_id))

@login_required
def book_del(request, book_id):
    """書籍の削除"""
    #     return HttpResponse('書籍の削除')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('day:book_list')



class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name='impressions'
    template_name='day/impression_list.html'
    paginate_by = 10  # １ページは最大2件ずつでページングする

    # @login_required
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])  # 親の書籍を読む
        impressions = book.impressions.all().order_by('id')   # 書籍の子供の、感想を読む
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)



@login_required
def impression_edit(request, book_id, impression_id=None):
    """感想の編集"""
    book = get_object_or_404(Book, pk=book_id)  # 親の書籍を読む
    if impression_id:   # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:               # impression_id が指定されていない (追加時)
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            impression = form.save(commit=False)
            impression.book = book  # この感想の、親の書籍をセット
            impression.save()
            return redirect('day:impression_list', book_id=book_id)
    else:    # GET の時
        form = ImpressionForm(instance=impression)  # impression インスタンスからフォームを作成

    return render(request,
                  'day/impression_edit.html',
                  dict(form=form, book_id=book_id, impression_id=impression_id))


@login_required
def impression_del(request, book_id, impression_id):
    """感想の削除"""
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return redirect('day:impression_list', book_id=book_id)

