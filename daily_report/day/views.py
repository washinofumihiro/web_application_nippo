from django.shortcuts import render, get_object_or_404, redirect
from .models import Report, Impression
from .forms import ReportForm, ImpressionForm, SearchForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from .forms import RegisterForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.db import IntegrityError
from . import user_config


def register(request):
    return render_to_response('day/register.html', {},
                              context_instance=RequestContext(request))


def create_user(request):
    user_id = request.POST['user_id']
    password = request.POST['password']
    mail_address = request.POST['mail_address']

    error_message = user_config.create_user(user_id, mail_address, password)

    if error_message:
        return render(request, 'day/register.html', {'error_message': error_message})
    else:
        return redirect('/')


@login_required
def report_list(request):
    """書籍の一覧"""
#    return HttpResponse('書籍の一覧')
    reports = Report.objects.all().order_by('id')
    form = SearchForm()
    # print(form)
    return render(request,
                  'day/report_list.html',     # 使用するテンプレート
                  {'reports': reports,'form': form})         # テンプレートに渡すデータ

# @login_required
# def report_browse(request):
#     """書籍の一覧"""
# #    return HttpResponse('書籍の一覧')
#     reports = Report.objects.all().order_by('id')
#     return render(request,
#                   'day/browse.html',     # 使用するテンプレート
#                   {'reports': reports})         # テンプレートに渡すデータ


@login_required
def report_edit(request, report_id=None):
    """書籍の編集"""
#     return HttpResponse('書籍の編集')
    date_object = datetime.now()

    if report_id:   # report_id が指定されている (修正時)
        report = get_object_or_404(Report, pk=report_id)
        if report.user != request.user.username:
            print(report.user)
            print(request.user)
            print("あなたが投稿した日報でありません。")
            return render(request, 'day/report_list.html', {'reports': Report.objects.all().order_by('id')})
    else:         # report_id が指定されていない (追加時)
        report = Report()
        report.user = request.user.username
    # print(report.user)
    # print(report.user_post_time)

    # data = Report.objects.get(id=30)
    # print(data)
    # print(reports.user)

    # data = get_object_or_404(Report)
    # for test in data:
    #     if test.user == request.user.username:
    #         print("succes")
    #         # print(test.objects.all().order_by('id'))

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            report = form.save(commit=False)
            report.user_post_time = datetime(*date_object.timetuple()[:6])
            report.save()
            return redirect('day:report_list')
    else:    # GET の時
        form = ReportForm(instance=report)  # report インスタンスからフォームを作成
        # inst = modelformset_factory(Report, exclude=('title',))
        # form = ReportForm(instance=inst)
        # form = ReportViewForm  # report インスタンスからフォームを作成


    return render(request, 'day/report_edit.html', dict(form=form, report_id=report_id))


@login_required
def report_browse(request, report_id=None):
    """書籍の編集"""
#     return HttpResponse('書籍の編集')
    if report_id:   # report_id が指定されている (修正時)
        report = get_object_or_404(Report, pk=report_id)
    else:         # report_id が指定されていない (追加時)
        report = Report()

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            report = form.save(commit=False)
            report.save()
            return redirect('day:report_list')
    else:    # GET の時
        form = ReportForm(instance=report)  # report インスタンスからフォームを作成

    return render(request, 'day/report_browse.html', dict(form=form, report_id=report_id))


@login_required
def report_del(request, report_id):
    """書籍の削除"""
    #     return HttpResponse('書籍の削除')
    report = get_object_or_404(Report, pk=report_id)
    report.delete()
    return redirect('day:report_list')



class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name='impressions'
    template_name='day/impression_list.html'
    paginate_by = 10  # １ページは最大2件ずつでページングする

    # @login_required
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(Report, pk=kwargs['report_id'])  # 親の書籍を読む
        impressions = report.impressions.all().order_by('id')   # 書籍の子供の、感想を読む
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, report=report)
        return self.render_to_response(context)



@login_required
def impression_edit(request, report_id, impression_id=None):
    """感想の編集"""
    date_object = datetime.now()
    report = get_object_or_404(Report, pk=report_id)  # 親の書籍を読む
    if impression_id:   # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:               # impression_id が指定されていない (追加時)
        impression = Impression()
        impression.comment_user = request.user.username

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            impression = form.save(commit=False)
            impression.report = report  # この感想の、親の書籍をセット
            impression.comment_time = datetime(*date_object.timetuple()[:6])
            impression.save()
            return redirect('day:impression_list', report_id=report_id)
    else:    # GET の時
        form = ImpressionForm(instance=impression)  # impression インスタンスからフォームを作成

    return render(request,
                  'day/impression_edit.html',
                  dict(form=form, report_id=report_id, impression_id=impression_id))


@login_required
def impression_del(request, report_id, impression_id):
    """感想の削除"""
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return redirect('day:impression_list', report_id=report_id)




#検索フォームの作成
def report_search(request):
    # report = get_object_or_404(Report)
    # print(report)
    # if report.user != request.user.username:
    #     print(report.user)
    #     print(request.user)
    #     print("あなたが投稿した日報でありません。")
    #     return render(request, 'day/report_list.html', {'reports': Report.objects.all().order_by('id')})

    # query = "iii"
    if request.method == 'GET':
        # print(request.POST)
        #form = request.POST['Search']
        # print(form)
        # print(form[''])

        form = SearchForm(request.GET)
        # print(request.POST)
        # print(form)
        reports = Report.objects.all().order_by('id')

        if form.is_valid():
            # print(form.cleaned_data["Search"])
            # print(request.GET['Search'])
            # keyword = request.POST['Search'].split()
            keyword = form.cleaned_data['Search'].split()
            # print(keyword)


            # チェックボックスにチェックがある場合はキーワードから各カラムを検索
            if request.GET.getlist('search_form'):
                query = Q()
                for data in request.GET.getlist('search_form'):
                    if data == 'user_post_time':
                        queries = [Q(user_post_time__icontains=word) for word in keyword]
                        # query = queries.pop(0)
                        for item in queries:
                            query |= item
                        # reports = Report.objects.filter(query)

                    elif data == 'user':
                        queries = [Q(user__icontains=word) for word in keyword]
                        # query = queries.pop(0)
                        for item in queries:
                            query |= item
                        # reports = Report.objects.filter(query)

                    elif data == 'title':
                        queries = [Q(title__icontains=word) for word in keyword]
                        # query = queries.pop(0)
                        for item in queries:
                            query |= item
                        # reports = Report.objects.filter(query)

                    elif data == 'content':
                        queries = [Q(content__icontains=word) for word in keyword]
                        # query = queries.pop(0)
                        for item in queries:
                            query |= item
                        # reports = Report.objects.filter(query)
                reports = Report.objects.filter(query).order_by('id')


            # チェックボックスにチェックがない場合はキーワードからDB内全検索
            else:
                queries1 = [Q(user_post_time__icontains=word) for word in keyword]
                queries2 = [Q(user__icontains=word) for word in keyword]
                queries3 = [Q(title__icontains=word) for word in keyword]
                queries4 = [Q(content__icontains=word) for word in keyword]

                query = queries1.pop(0)

                # print(query)
                # print()
                # print(queries1)
                # print()

                for item in queries1:
                    query |= item
                for item in queries2:
                    query |= item
                for item in queries3:
                    query |= item
                for item in queries4:
                    query |= item

                # print(query)
                # print()
                reports = Report.objects.filter(query).order_by('id')

            #
            # for data in request.POST.getlist('search_form'):
            #     if data == 'user_post_time':
            #         reports = reports.filter(user_post_time__icontains=form.cleaned_data["Search"]).order_by('id')
            #     elif data == 'user':
            #         reports = reports.filter(user__icontains=form.cleaned_data["Search"]).order_by('id')
            #     elif data == 'title':
            #         reports = reports.filter(title__icontains=form.cleaned_data["Search"]).order_by('id')
            #     elif data == 'content':
            #         reports = reports.filter(content__icontains=form.cleaned_data["Search"]).order_by('id')

            # reports = Report.objects.filter(user = form.cleaned_data["Search"]).order_by('id')

            return render(request,
                      'day/report_list.html',     # 使用するテンプレート
                      {'reports': reports, 'form': form, 'word':request.GET['Search']})         # テンプレートに渡すデータ

        else:#入力がない場合
            reports = Report.objects.all().order_by('id')
            return render(request,
                      'day/report_list.html',  # 使用するテンプレート
                      {'reports': reports, 'form': form})  # テンプレートに渡すデータ

    else:  #検索フォームを押さない場合
        reports = Report.objects.all().order_by('id')
        return render(request,
                  'day/report_list.html',  # 使用するテンプレート
                  {'reports': reports})  # テンプレートに渡すデータ
