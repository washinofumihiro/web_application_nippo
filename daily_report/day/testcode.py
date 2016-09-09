# -*- coding: utf-8 -*-
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


# ユーザの作成
def create_user(self, username, password):
    return User.objects.create_user(username=username, email=None, password=password)


# 日報の作成
def create_report(self, title, content, user, time):
    return Report.objects.create(title=title, content=content, user=user, user_post_time=time)


# 日報の削除
def delete_report(self, report_id):
    Report.objects.get(id=report_id).delete()


# 日報に対してのコメントの作成
def create_impression(self, report, comment, comment_user, comment_time):
    return Impression.objects.create(report=report, comment=comment, comment_user=comment_user,
                                     comment_time=comment_time)

# コメントの削除
def delete_impression(self, impression_id):
    Report.objects.get(id=impression_id).delete()

class UserTest(TestCase):
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
        print("Success test")

        # ユーザが正しく作成されるか確認

    def test_make_user(self):
        # ユーザの作成と呼び出し
        user_1 = create_user(self, self.user_id[0], self.password[0])
        user_2 = create_user(self, self.user_id[1], self.no_password)

        # 作成したユーザのIDとパスワードが一致しているか確認
        # ID、パスワード共に入力されたとき
        self.assertEquals(user_1.username, self.user_id[0])
        self.assertTrue(user_1.check_password(self.password[0]))

        # IDは入力され、パスワードが入力されなかったとき
        self.assertEquals(user_2.username, self.user_id[1])
        self.assertTrue(user_2.check_password(self.no_password))

        # IDに入力がない場合、ユーザーが作成されないかどうか

    def test_not_make_user(self):
        # 設定するIDとパスワード
        # no_user_id = ''
        # no_password = ''

        # ユーザが作成できないことを確認
        self.assertRaises(ValueError, lambda: User.objects.create_user(self.no_user_id, None, self.no_password))

        # 作成したユーザがログインできるかどうか

    def test_login(self):
        # ユーザを作成
        create_user(self, self.user_id[0], self.password[0])

        # 作成したユーザでログインできるかを確認
        client_user = Client()
        self.assertTrue(client_user.login(username=self.user_id[0], password=self.password[0]))

        # 異なるID、パスワードでログインできないかどうか

    def test_not_login(self):
        # ユーザを作成
        create_user(self, self.user_id[0], self.password[0])

        # 作成したユーザに異なるパスワードでログインできないかを確認
        client_user = Client()
        self.assertFalse(client_user.login(username=self.user_id[0], password=self.error_password))


class ReportTest(TestCase):
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
        print("Success test")

    # @classmethod
    # def setUpTestData(cls):
    #     print("----setuptestdata")

    #データベースの初期状態の確認(何も入力されていないか確認)
    def test_init_database(self):
        saved_report = Report.objects.all()
        self.assertEquals(saved_report.count(), 0)


    #日報の各項目が正しく入力され、また、削除できるか確認
    def test_report_add(self):
        #各データの入力と呼び出し
        report = create_report(self, self.title[0], self.content[0], self.user[0], self.time[0])

        #各データが一致しているかを確認
        self.assertEquals(report.title, self.title[0])
        self.assertEquals(report.content, self.content[0])
        self.assertEquals(report.user, self.user[0])
        self.assertEquals(report.user_post_time, self.time[0])

        #日報の削除
        report_id = report.id
        # print(report_id)
        report = delete_report(self, report_id)

        # 各データが削除されているかを確認
        # self.assertRaises(ValueError, lambda: User.objects.create_user(self.no_user_id, None, self.no_password))
        self.assertRaises(AttributeError, lambda : report.title)
        self.assertRaises(AttributeError, lambda : report.content)
        self.assertRaises(AttributeError, lambda : report.user)
        self.assertRaises(AttributeError, lambda : report.time)
        self.assertEquals(report, None)



class CommentTest(TestCase):
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
        print("Success test")

    #コメントが正しく入力され、また、削除できるかを確認
    def test_immpression_add(self):
        report = create_report(self, self.title[0], self.content[0], self.user[0], self.time[0])
        comment = create_impression(self, report, self.comment[0], self.comment_user[0], self.comment_time[0])

        #各日報にコメントが入力されているかを確認
        self.assertEquals(comment.comment, self.comment[0])
        self.assertEquals(comment.comment_user, self.comment_user[0])
        self.assertEquals(comment.comment_time, self.comment_time[0])

        #コメントの削除
        report_id = report.id
        comment_id = Report.objects.all().prefetch_related("impressions").get(id=report_id).impressions.values()[0]['id']
        comment = delete_impression(self, comment_id)

        # 各データが削除されているかを確認
        # self.assertRaises(ValueError, lambda: User.objects.create_user(self.no_user_id, None, self.no_password))
        self.assertRaises(AttributeError, lambda : comment.comment)
        self.assertRaises(AttributeError, lambda : comment.comment_user)
        self.assertRaises(AttributeError, lambda : comment.comment_time)
        self.assertEquals(comment, None)

class UrlAuthTest(TestCase):
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

        cls.transition_url = ['report/', 'report/add/', '/day/report/search/',
                              'report/mod/', 'report/browse/',
                              'impression/', 'impression/add/',
                              'impression/mod/']
        cls.redirect_request_url = ['/day/report/del/1/', '/day/impression/del/2/2/']
        cls.redirect_response_url = ['/day/report/', '/day/impression/2/']

        cls.search_keyword = 'Terry'

    @classmethod
    def tearDownClass(cls):
        print("Success test")

    #日報に対して
    #ユーザ認証テスト
    #ログイン状態によるページへのアクセスの可否をテスト
    def test_auth(self):
        #ユーザの作成
        create_user(self, self.user_id[0], self.password[0])
        client_user = Client()
        client_user.login(username=self.user_id[0], password=self.password[0])

       # データベースを作成
        report = create_report(self, self.title[0], self.content[0], self.user[0], self.time[0])
        for i in range(1, len(self.title)):
            create_report(self, self.title[i], self.content[i], self.user[i], self.time[i])

        start_report_id = report.id

        for i in range(len(self.comment)):
            init_report = Report.objects.get(id=start_report_id + i)
            comment = create_impression(self, init_report, self.comment[i], self.comment_user[i], self.comment_time[i])
        comment_id = comment.id
        # ページ遷移できているかを確認
        base_url = '/day/'

        for i in self.transition_url:
            if i=='report/mod/' or i=='report/browse/' or i=='impression/' or i=='impression/add/':
                url = base_url + i + str(start_report_id) + '/'
            elif i=='report/mod/':
                url = base_url + i + str(start_report_id) + '/' + str(comment_id) + '/'
            else:
                url = base_url + i
            response_data = client_user.get(url)
            self.assertEqual(response_data.status_code, 200)

        # # リダイレクトできているかを確認
        # for i in range(len(self.redirect_request_url)):
        #     if self.redirect_request_url[i] == 'report/del/':
        #         url =base_url + self.redirect_request_url[i] + str(start_report_id)
        #     elif self.redirect_request_url[i] == 'impression/del/':
        #     response_data = client_user.get(self.redirect_request_url[i])
        #     self.assertRedirects(response_data, self.redirect_response_url[i])


        #
        # # 日報に対して
        # # ユーザ認証テスト
        # # ログイン状態によるページへのアクセスの可否をテスト
        # def test_auth(self):
        #     # ユーザの作成
        #     create_user(self, self.user_id[0], self.password[0])
        #     client_user = Client()
        #     client_user.login(username=self.user_id[0], password=self.password[0])
        #
        #     # データベースを作成
        #     for i in range(len(self.title)):
        #         create_report(self, self.title[i], self.content[i], self.user[i], self.time[i])
        #
        #     for i in range(len(self.comment)):
        #         init_report = Report.objects.get(id=i + 1)
        #         create_impression(self, init_report, self.comment[i], self.comment_user[i], self.comment_time[i])
        #
        #     # ページ遷移できているかを確認
        #     for i in range(len(self.transition_url)):
        #         response_data = client_user.get(self.transition_url[i])
        #         self.assertEqual(response_data.status_code, 200)
        #
        #     # リダイレクトできているかを確認
        #     for i in range(len(self.redirect_request_url)):
        #         response_data = client_user.get(self.redirect_request_url[i])
        #         self.assertRedirects(response_data, self.redirect_response_url[i])


class SearchTest(TestCase):
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
                              '/day/report/mod/1/', '/day/report/browse/1/',
                              '/day/impression/1/', '/day/impression/add/1/',
                              '/day/impression/mod/1/1/']
        cls.redirect_request_url = ['/day/report/del/1/', '/day/impression/del/2/2/']
        cls.redirect_response_url = ['/day/report/', '/day/impression/2/']

        cls.search_keyword = 'Terry'

    @classmethod
    def tearDownClass(cls):
        print("Success test")

    # 検索機能できるかどうかのテスト
    def test_search(self):
        #テストコード内の検索に使用するキーワード
        # keyword = 'Terry'

        #データベースを作成
        for i in range(len(self.title)):
            create_report(self, self.title[i], self.content[i], self.user[i], self.time[i])

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



