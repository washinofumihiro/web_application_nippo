from django.test import TestCase
from .models import Report, Impression
from . import forms
from . import views
from django.contrib.auth.models import User
from django.test.client import Client
from django.http import HttpRequest
from . import models
from django.db.models import Q


class ReportTest(TestCase):

    #データベースの初期状態の確認(何も入力されないかどうか)
    def test_init_database(self):
        saved_report = Report.objects.all()
        self.assertEquals(saved_report.count(),0)

    #日報の各項目が正しく入力されているかどうか
    def test_report_add(self):

        #各項目の入力データ
        first_report = Report()
        title = 'report'
        content = 'content'
        user = 'user'
        time = '2016-08-24 15:43:06'

        #各項目への入力
        first_report.title = title
        first_report.content = content
        first_report.user = user
        first_report.user_post_time = time
        first_report.save()

        #登録した各項目を呼び出し
        saved_report = Report.objects.all()
        actual_report = saved_report[0]

        #各データが一致しているかを確認
        self.assertEquals(actual_report.title,title)
        self.assertEquals(actual_report.content, content)
        self.assertEquals(actual_report.user,user )
        self.assertEquals(actual_report.user_post_time, time)

    #ユーザが正しく作成されるかどうか
    def test_make_user(self):

        #設定するIDとパスワード
        user_id_1 = 'user1'
        user_id_2 = 'user2'
        password = 'password'
        no_password = ''

        #ユーザの作成
        new_user = User.objects.create_user(user_id_1, None, password)
        new_user = User.objects.create_user(user_id_2, None, no_password)
        new_user.save()

        #作成したユーザ情報を呼び出し
        saved_user = User.objects.all()
        actual_user_1 = saved_user[0]
        actual_user_2 = saved_user[1]
        # print(actual_user_1)
        # print(actual_user_2)

        #作成したユーザのIDとパスワードが一致しているか確認
        #ID、パスワード共に入力されたとき
        self.assertEquals(actual_user_1.username,user_id_1)
        self.assertTrue(actual_user_1.check_password(password))

        #IDは入力され、パスワードが入力されなかったとき
        self.assertEquals(actual_user_2.username, user_id_2)
        self.assertTrue(actual_user_2.check_password(no_password))

    #IDに入力がない場合、ユーザーが作成されないかどうか
    def test_not_make_user(self):
        #設定するIDとパスワード
        no_user_id = ''
        no_password = ''

        #ユーザの作成
        self.assertRaises(ValueError, lambda: User.objects.create_user(no_user_id, None,no_password))

    #作成したユーザがログインできるかどうか
    def test_login(self):
        #ログインするユーザ情報(ID、パスワード)
        user_id = 'user'
        password = 'password'

        #ユーザを作成
        new_user = User.objects.create_user(user_id, None, password)
        new_user.save()
        # self.assertIsNotNone(new_user)

        #作成したユーザでログインできるかを確認
        client_user = Client()
        self.assertTrue(client_user.login(username = user_id, password = password))

    #異なるID、パスワードでログインできないかどうか
    def test_not_login(self):
        # ログインするユーザ情報(ID、パスワード)
        user_id = 'user'
        password = 'password'

        # ユーザを作成
        new_user = User.objects.create_user(user_id, None, password)
        new_user.save()
        # self.assertIsNotNone(new_user)

        # 作成したユーザに異なるパスワードでログインできないかを確認
        client_user = Client()
        self.assertFalse(client_user.login(username=user_id, password='error_password'))


    # 検索機能できるかどうかのテスト
    def test_search(self):

        #データベースの入力データ
        title = ['report', 'test', 'daily']
        content = ['content', 'text', 'plan']
        user = ['Terry', 'Dai', 'Allen']
        time = ['2006-04-01 12:34:56', '2010-12-25 00:00:00', '2016-08-24 15:43:06']

        #テストコード内の検索に使用するキーワード
        keyword = 'Terry'

        #データベースを作成
        for i in range(len(title)):
            Report.objects.create(title=title[i], content=content[i], user=user[i], user_post_time=time[i])

        # #登録した各項目を呼び出し
        # input_report = Report.objects.all()

        #データベース入力の別の方法
        # #クラスを直接使う
        # for i in range(len(title)):
        #     Report(title=title[i], content=content[i], user=user[i], user_post_time=time[i]).save()

        # # 登録した各項目を呼び出し
        # input_report = Report.objects.all()
        # for i in input_report:
        #     print(i.title, i.content, i.user, i.user_post_time)


        #検索ページ(report_list.html)の呼び出し
        c = Client()
        # response = c.post('/', {'username': 'Terry', 'password': 'password'})
        # response.status_code

        response_data = c.post('/day/report/search/', {'Search': keyword})
        # print(response_data.context)
        # print(response_data.context['word'])
        # print(response_data.context['reports'])   #そのままではエラー
        # for i in response_data.content:
        #     print(i)

        #確認用
        # for  i in response_data.context['reports']:
        #     print(i.title, i.content, i.user, i.user_post_time)


        #テストコード内でフィルターをかける
        #ほとんどviews.report_searchと同じ
        keyword = keyword.split()
        queries1 = [Q(user_post_time__icontains=word) for word in keyword]
        queries2 = [Q(user__icontains=word) for word in keyword]
        queries3 = [Q(title__icontains=word) for word in keyword]
        queries4 = [Q(content__icontains=word) for word in keyword]
        query = queries1.pop(0)

        for item in queries1:
            query |= item
        for item in queries2:
            query |= item
        for item in queries3:
            query |= item
        for item in queries4:
            query |= item

        input_report = Report.objects.filter(query).order_by('id')

        #確認用
        # for i in input_report:
        #     print(i.title, i.content, i.user, i.user_post_time)

        #Searchクラスが正常に検索できているかをテスト
        for i,j in zip(response_data.context['reports'], input_report):
            self.assertEquals(i.title, j.title)
            self.assertEquals(i.content, j.content)
            self.assertEquals(i.user, j.user)
            self.assertEquals(i.user_post_time, j.user_post_time)



