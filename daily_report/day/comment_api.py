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
from . import report_api


def list(report_id):
    # reports = Report.objects.all().order_by('id')
    # print(reports.title)
    # report = get_object_or_404(Report, pk=kwargs['report_id'])  # 親の書籍を読む
    # print(report_id)
    comment = Report.objects.all().prefetch_related("impressions").get(id=report_id).impressions.all()
    # print(comment)
    # comment = report.impressions.all().order_by('id')
    return comment
#
# class ImpressionList(ListView):
#     """感想の一覧"""
#     context_object_name='impressions'
#     template_name='day/impression_list.html'
#     paginate_by = 10  # １ページは最大2件ずつでページングする
#
#     # @login_required
#     def get(self, request, *args, **kwargs):
#         report = get_object_or_404(Report, pk=kwargs['report_id'])  # 親の書籍を読む
#         impressions = report.impressions.all().order_by('id')   # 書籍の子供の、感想を読む
#         self.object_list = impressions
#
#         context = self.get_context_data(object_list=self.object_list, report=report)
#         return self.render_to_response(context)


# 日報のフォーム指定
def show(comment_id, login_user):
    if comment_id:   # report_id が指定されている (修正時)
        comment = get_object_or_404(Impression, pk=comment_id)
    else:         # report_id が指定されていない (追加時)
        comment = Impression()
        comment.comment_user = login_user

    return comment


def edit(post_data, comment, report_id):
    date_object = datetime.now()
    report = get_object_or_404(Report, pk=report_id)
    form = ImpressionForm(post_data, instance=comment)  # POST された request データからフォームを作成
    if form.is_valid():  # フォームのバリデーション
        comment = form.save(commit=False)
        comment.report = report
        comment.commnet_time = datetime(*date_object.timetuple()[:6])
        comment.save()
    return form


def delete(comment_id):
    comment = get_object_or_404(Impression, pk=comment_id)
    comment.delete()


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

