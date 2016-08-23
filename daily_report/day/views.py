from django.shortcuts import render, get_object_or_404, redirect
from .models import Report, Impression
from .forms import ReportForm, ImpressionForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from .forms import RegisterForm
from django.template import RequestContext
from django.shortcuts import render_to_response


# @require_GET
# def _new(request):
#     form = CustomUserCreationForm()
#     c = {'form': form}
#     c.update(csrf(request))
#     return render_to_response('three/user_new.html', c, mimetype='text/html'

# def registor(request):
#     form = UserForm()
#     return render(request,'day/registor.html', {'fom':form})


# def regist(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         'form': form,
#     }
#     return render(request, 'day/regist.html', context)
#
# @require_POST
# def regist_save(request):
#     form = RegisterForm(request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect('day:index')
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'main/regist.html', context)
#
#
# def index(request):
#     context = {
#         'user': request.user,
#     }
#     return render(request, 'day/index.html', context)
#

def index(request):
    return render_to_response('day/login.html', {},
            context_instance=RequestContext(request))


def register(request):
    return render_to_response('day/register.html', {},
            context_instance=RequestContext(request))


def create_user(request):
    user_id = request.POST['user_id']
    password = request.POST['password']

    new_user = User.objects.create_user(user_id, None, password)
    new_user.save()

    return redirect('/')



@login_required
def report_list(request):
    """書籍の一覧"""
#    return HttpResponse('書籍の一覧')
    reports = Report.objects.all().order_by('id')
    return render(request,
                  'day/report_list.html',     # 使用するテンプレート
                  {'reports': reports})         # テンプレートに渡すデータ

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



    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            report = form.save(commit=False)
            report.save()
            return redirect('day:report_list')
    else:    # GET の時
        form = ReportForm(instance=report)  # report インスタンスからフォームを作成

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
    report = get_object_or_404(Report, pk=report_id)  # 親の書籍を読む
    if impression_id:   # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:               # impression_id が指定されていない (追加時)
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            impression = form.save(commit=False)
            impression.report = report  # この感想の、親の書籍をセット
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

