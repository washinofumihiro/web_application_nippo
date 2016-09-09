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
import hashlib
import random
from django.core.exceptions import ObjectDoesNotExist


class ReportTest(TestCase):
    # def setUp(self):
    #     print("setup")
    #
    # def tearDown(self):
    #     print("teardown")
    #テスト開始時にテストデータを初期化
    @classmethod
    def setUpClass(cls):
        print("setupclass")
        cls.user_id = ['Terry', 'Dai', 'Allen']
        cls.no_user_id = ""
        cls.password = cls.user_id
        cls.no_password = ""
        cls.error_password = "error_password"

        cls.title = ['report', 'test', 'daily']
        cls.content = ['content', 'text', 'plan']
        cls.user = cls.user_id
        cls.time = ['2006-04-01 12:34:56', '2010-12-25 00:00:00', '2016-08-24 15:43:06']

        cls.comment = ['Great', 'Good', 'Bad']
        cls.comment_user = ['Allen', 'Terry', 'Dai']
        cls.comment_time = ['2010-12-25 00:00:00', '2016-08-24 15:43:06', '2006-04-01 12:34:56']

        cls.transition_url = ['/day/report/', '/day/report/add/', '/day/report/search/',
                    '/day/report/mod/1/',  '/day/report/browse/1/',
                    '/day/impression/1/', '/day/impression/add/1/',
                    '/day/impression/mod/1/1/']
        cls.redirect_request_url = ['/day/report/del/1/', '/day/impression/del/2/2/']
        cls.redirect_response_url = ['/day/report/', '/day/impression/2/']

        cls.search_keyword = 'Terry'

    @classmethod
    def tearDownClass(cls):
        print("END test")


    # @classmethod
    # def setUpTestData(cls):
    #     print("----setuptestdata")

    #ユーザの作成
    def create_user(self, username, password):
        return User.objects.create_user(username=username, email=None, password=password)

    #日報の作成
    def create_report(self, title, content, user, time):
        return Report.objects.create(title=title, content=content, user=user, user_post_time=time)

    #日報の削除
    def delete_report(self, report_id):
        Report.objects.get(id=report_id).delete()

    #日報に対してのコメントの作成
    def create_impression(self, report, comment, comment_user, comment_time):
        return Impression.objects.create(report=report, comment=comment, comment_user=comment_user,
                                  comment_time=comment_time)

    def delete_impression(self, impression_id):
        Report.objects.get(id=impression_id).delete()

    #データベースの初期状態の確認(何も入力されていないか確認)
    def test_init_database(self):
        saved_report = Report.objects.all()
        self.assertEquals(saved_report.count(), 0)

    #ユーザが正しく作成されるか確認
    def test_make_user(self):

        #設定するIDとパスワード
        # user_id_1 = 'user1'
        # user_id_2 = 'user2'
        # password = 'password'
        # no_password = ''

        #ユーザの作成と呼び出し
        user_1 = self.create_user(self.user_id[0], self.password[0])
        user_2 = self.create_user(self.user_id[1], self.no_password)

        #作成したユーザのIDとパスワードが一致しているか確認
        #ID、パスワード共に入力されたとき
        self.assertEquals(user_1.username, self.user_id[0])
        self.assertTrue(user_1.check_password(self.password[0]))

        #IDは入力され、パスワードが入力されなかったとき
        self.assertEquals(user_2.username, self.user_id[1])
        self.assertTrue(user_2.check_password(self.no_password))

    #IDに入力がない場合、ユーザーが作成されないかどうか
    def test_not_make_user(self):
        #設定するIDとパスワード
        # no_user_id = ''
        # no_password = ''

        #ユーザが作成できないことを確認
        self.assertRaises(ValueError, lambda: User.objects.create_user(self.no_user_id, None, self.no_password))

    #作成したユーザがログインできるかどうか
    def test_login(self):
        #ログインするユーザ情報(ID、パスワード)
        # user_id = 'user'
        # password = 'password'

        #ユーザを作成
        self.create_user(self.user_id[0], self.password[0])

        #作成したユーザでログインできるかを確認
        client_user = Client()
        self.assertTrue(client_user.login(username=self.user_id[0], password=self.password[0]))

    #異なるID、パスワードでログインできないかどうか
    def test_not_login(self):
        # ログインするユーザ情報(ID、パスワード)
        # user_id = 'user'
        # password = 'password'

        # ユーザを作成
        self.create_user(self.user_id[0], self.password[0])

        # 作成したユーザに異なるパスワードでログインできないかを確認
        client_user = Client()
        self.assertFalse(client_user.login(username=self.user_id[0], password=self.error_password))

    #日報の各項目が正しく入力され、また、削除できるか確認
    def test_report_add(self):
        #各データの入力と呼び出し
        report = self.create_report(self.title[0], self.content[0], self.user[0], self.time[0])

        #各データが一致しているかを確認
        self.assertEquals(report.title, self.title[0])
        self.assertEquals(report.content, self.content[0])
        self.assertEquals(report.user, self.user[0])
        self.assertEquals(report.user_post_time, self.time[0])

        #日報の削除
        report_id = report.id
        # print(report_id)
        report = self.delete_report(report_id)

        # 各データが削除されているかを確認
        # self.assertRaises(ValueError, lambda: User.objects.create_user(self.no_user_id, None, self.no_password))
        self.assertRaises(AttributeError, lambda : report.title)
        self.assertRaises(AttributeError, lambda : report.content)
        self.assertRaises(AttributeError, lambda : report.user)
        self.assertRaises(AttributeError, lambda : report.time)
        self.assertEquals(report, None)
        # self.assertEquals(report.title, self.title[0])
        # self.assertEquals(report.content, self.content[0])
        # self.assertEquals(report.user, self.user[0])
        # self.assertEquals(report.user_post_time, self.time[0])

    #コメントが正しく入力され、また、削除できるかを確認
    def test_immpression_add(self):
        report = self.create_report(self.title[0], self.content[0], self.user[0], self.time[0])
        comment = self.create_impression(report, self.comment[0], self.comment_user[0], self.comment_time[0])

        #各日報にコメントが入力されているかを確認
        self.assertEquals(comment.comment, self.comment[0])
        self.assertEquals(comment.comment_user, self.comment_user[0])
        self.assertEquals(comment.comment_time, self.comment_time[0])

        #コメントの削除
        report_id = report.id
        # print(report_id)
        # comment_id = comment.id
        # aa = Report.objects.all()
        # print(aa.count())

        comment_id = Report.objects.all().prefetch_related("impressions").get(id=report_id).impressions.values()[0]['id']
        comment = self.delete_impression(comment_id)

        # 各データが削除されているかを確認
        # self.assertRaises(ValueError, lambda: User.objects.create_user(self.no_user_id, None, self.no_password))
        self.assertRaises(AttributeError, lambda : comment.comment)
        self.assertRaises(AttributeError, lambda : comment.comment_user)
        self.assertRaises(AttributeError, lambda : comment.comment_time)
        self.assertEquals(comment, None)

    #日報に対して
    #ユーザ認証テスト
    #ログイン状態によるページへのアクセスの可否をテスト
    def test_auth(self):
        # データベースの入力データ
        # ログインするユーザ情報(ID、パスワード)
        # user_id = 'Terry'
        # password = 'password'
        # title = ['report', 'test', 'daily']
        # content = ['content', 'text', 'plan']
        # user = ['Terry', 'Dai', 'Allen']
        # time = ['2006-04-01 12:34:56', '2010-12-25 00:00:00', '2016-08-24 15:43:06']
        # comment = ['Great', 'Good', 'Bad']
        # comment_user = ['Allen', 'Terry', 'Dai']
        # comment_time = ['2010-12-25 00:00:00', '2016-08-24 15:43:06', '2006-04-01 12:34:56']

        #ユーザの作成
        self.create_user(self.user_id[0], self.password[0])
        client_user = Client()
        client_user.login(username=self.user_id[0], password=self.password[0])

       # データベースを作成
        for i in range(len(self.title)):
            self.create_report(self.title[i], self.content[i], self.user[i], self.time[i])
        # test = Report.objects.all()
        # print(test.count())

        # self.delete_report(1)
        # test.get(id=1).delete()
        # Report.objects.get(id=1).delete()
        # test = Report.objects.all()

        # test = Report.objects.all()
        # print(test.count())

        for i in range(len(self.comment)):
            init_report = Report.objects.get(id=i+1)
            self.create_impression(init_report, self.comment[i], self.comment_user[i], self.comment_time[i])
            # print(aaa.comment)
            # print(aaa.comment_user)
            # print(aaa.comment_time)

        # self.create_impression(init_report, 'So bad', self.comment_user[i], self.comment_time[i])
        # abc = Report.objects.get(pk=1)
        # print(abc.title)


        # i=0
        # # bbb = Report.objects.all().values()
        # # print(bbb)
        # for campaign in Report.objects.all().prefetch_related("impressions"):
        #     i=i+1
        #     # print(campaign.impressions.get(id=i))
        #     # print(campaign.impressions.get(pk=1))
        #     # print(campaign.impressions.get(id=i).comment)
        #     # print(campaign.impressions.get(id=i).comment_user)
        #     # print(campaign.impressions.values())
        #     # # print(campaign.impressions.get(id=i))
        #     # print()
        #     # print(Report.objects.all().prefetch_related("impressions")[i-1].impressions.values())
        #
        # print()
        # print()

        # #コメントの削除
        # #指定した日報の新しいコメントのidを取得
        # delete_comment_number = Report.objects.all().prefetch_related("impressions")[1].impressions.values()[0]['id']
        # self.delete_impression(delete_comment_number)

            # print(campaign.impressions.comment_user[0])
        # data = init_report.impression_set.all()
        #
        # print(data[0].id)
        # aaa = Report.objects.all().prefetch_related("impressions")
        # print(aaa.impressions[0])

        #ログインしてページ遷移できるかを確認
        # transition_url = ['/day/report/', '/day/report/add/', '/day/report/search/',
        #             '/day/report/mod/1/',  '/day/report/browse/1/',
        #             '/day/impression/1/', '/day/impression/add/1/',
        #             '/day/impression/mod/1/1/']

        for i in range(len(self.transition_url)):
            response_data = client_user.get(self.transition_url[i])
            self.assertEqual(response_data.status_code, 200)

        #リダイレクトできているかを確認
        # response_data = client_user.get('/day/report/del/1/')
        # self.assertRedirects(response_data, '/day/report/')
        # response_data = client_user.get('/day/impression/del/2/2/')
        # self.assertRedirects(response_data, '/day/impression/2/')

        for i in range(len(self.redirect_request_url)):
            response_data = client_user.get(self.redirect_request_url[i])
            self.assertRedirects(response_data, self.redirect_response_url[i])


    # 検索機能できるかどうかのテスト
    def test_search(self):
        # #データベースの入力データ
        # title = ['report', 'test', 'daily']
        # content = ['content', 'text', 'plan']
        # user = ['Terry', 'Dai', 'Allen']
        # time = ['2006-04-01 12:34:56', '2010-12-25 00:00:00', '2016-08-24 15:43:06']

        #テストコード内の検索に使用するキーワード
        # keyword = 'Terry'

        #データベースを作成
        for i in range(len(self.title)):
            self.create_report(self.title[i], self.content[i], self.user[i], self.time[i])

        #検索ページ(report_list.html)の呼び出し
        client_user = Client()
        response_data = client_user.post('/day/report/search/', {'Search': self.search_keyword})

        #確認用
        # for  i in response_data.context['reports']:
        #     print(i.title, i.content, i.user, i.user_post_time)

        #テストコード内でフィルターをかける
        #ほとんどviews.report_searchと同じ
        keyword = self.search_keyword.split()
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



