from django.test import TestCase
from .models import Report, Impression
from . import forms
from . import views
from django.contrib.auth.models import User
from django.test.client import Client
from django.http import HttpRequest
from . import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory
from django.contrib.auth import authenticate


class ReportTest(TestCase):
    #ユーザの作成
    def create_user(self, username, password):
        return User.objects.create_user(username, None, password)

    #日報の作成
    def create_report(self, title, content, user, time):
        return Report.objects.create(title=title, content=content, user=user, user_post_time=time)

    #日報に対してのコメントの作成
    def create_impression(self, report, comment, comment_user, comment_time):
        return Impression.objects.create(report=report, comment=comment, comment_user=comment_user,
                                  comment_time=comment_time)

    #データベースの初期状態の確認(何も入力されていないか確認)
    def test_init_database(self):
        saved_report = Report.objects.all()
        self.assertEquals(saved_report.count(), 0)

    #日報の各項目が正しく入力されているか確認
    def test_report_add(self):

        #各項目の入力データ
        title = 'report'
        content = 'content'
        user = 'user'
        time = '2016-08-24 15:43:06'

        #各データの入力と呼び出し
        report = self.create_report(title, content, user, time)

        #各データが一致しているかを確認
        self.assertEquals(report.title, title)
        self.assertEquals(report.content, content)
        self.assertEquals(report.user, user)
        self.assertEquals(report.user_post_time, time)

    #ユーザが正しく作成されるか確認
    def test_make_user(self):

        #設定するIDとパスワード
        user_id_1 = 'user1'
        user_id_2 = 'user2'
        password = 'password'
        no_password = ''

        #ユーザの作成と呼び出し
        user_1 = self.create_user(user_id_1, password)
        user_2 = self.create_user(user_id_2, no_password)

        #作成したユーザのIDとパスワードが一致しているか確認
        #ID、パスワード共に入力されたとき
        self.assertEquals(user_1.username, user_id_1)
        self.assertTrue(user_1.check_password(password))

        #IDは入力され、パスワードが入力されなかったとき
        self.assertEquals(user_2.username, user_id_2)
        self.assertTrue(user_2.check_password(no_password))

    #IDに入力がない場合、ユーザーが作成されないかどうか
    def test_not_make_user(self):
        #設定するIDとパスワード
        no_user_id = ''
        no_password = ''

        #ユーザが作成できないことを確認
        self.assertRaises(ValueError, lambda: User.objects.create_user(no_user_id, None,no_password))

    #作成したユーザがログインできるかどうか
    def test_login(self):
        #ログインするユーザ情報(ID、パスワード)
        user_id = 'user'
        password = 'password'

        #ユーザを作成
        self.create_user(user_id, password)

        #作成したユーザでログインできるかを確認
        client_user = Client()
        self.assertTrue(client_user.login(username=user_id, password=password))

    #異なるID、パスワードでログインできないかどうか
    def test_not_login(self):
        # ログインするユーザ情報(ID、パスワード)
        user_id = 'user'
        password = 'password'

        # ユーザを作成
        self.create_user(user_id, password)

        # 作成したユーザに異なるパスワードでログインできないかを確認
        client_user = Client()
        self.assertFalse(client_user.login(username=user_id, password='error_password'))

    #ユーザ認証テスト
    #ログイン状態によるページへのアクセスの可否をテスト
    def test_auth(self):
        # データベースの入力データ
        # ログインするユーザ情報(ID、パスワード)
        user_id = 'Terry'
        password = 'password'
        title = ['report', 'test', 'daily']
        content = ['content', 'text', 'plan']
        user = ['Terry', 'Dai', 'Allen']
        time = ['2006-04-01 12:34:56', '2010-12-25 00:00:00', '2016-08-24 15:43:06']
        comment = ['Great', 'Good', 'Bad']
        comment_user = ['Allen', 'Terry', 'Dai']
        comment_time = ['2010-12-25 00:00:00', '2016-08-24 15:43:06', '2006-04-01 12:34:56']

        #ユーザの作成
        self.create_user(user_id, password)
        client_user = Client()
        client_user.login(username=user_id, password=password)

       # データベースを作成
        for i in range(len(title)):
            self.create_report(title[i], content[i], user[i], time[i])

        for i in range(len(comment)):
            init_report = Report.objects.get(id=i+1)
            self.create_impression(init_report, comment[i], comment_user[i], comment_time[i])

        #ログインしてページ遷移できるかを確認
        test_url = ['/day/report/', '/day/report/add/', '/day/report/search/',
                    '/day/report/mod/1/',  '/day/report/browse/1/',
                    '/day/impression/1/', '/day/impression/add/1/',
                    '/day/impression/mod/1/1/']

        for i in range(len(test_url)):
            response_data = client_user.get(test_url[i])
            self.assertEqual(response_data.status_code, 200)

        #リダイレクトできているかを確認
        response_data = client_user.get('/day/report/del/1/')
        self.assertRedirects(response_data, '/day/report/')
        response_data = client_user.get('/day/impression/del/2/2/')
        self.assertRedirects(response_data, '/day/impression/2/')


    # 検索機能できるかどうかのテスト
    def test_search(self):
        # #データベースの入力データ
        title = ['report', 'test', 'daily']
        content = ['content', 'text', 'plan']
        user = ['Terry', 'Dai', 'Allen']
        time = ['2006-04-01 12:34:56', '2010-12-25 00:00:00', '2016-08-24 15:43:06']

        #テストコード内の検索に使用するキーワード
        keyword = 'Terry'

        #データベースを作成
        for i in range(len(title)):
            self.create_report(title[i], content[i], user[i], time[i])

        #検索ページ(report_list.html)の呼び出し
        client_user = Client()


        response_data = client_user.post('/day/report/search/', {'Search': keyword})

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

        #Searchクラスが正常に検索できているかをテスト
        for i,j in zip(response_data.context['reports'], input_report):
            self.assertEquals(i.title, j.title)
            self.assertEquals(i.content, j.content)
            self.assertEquals(i.user, j.user)
            self.assertEquals(i.user_post_time, j.user_post_time)



