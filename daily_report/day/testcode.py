from django.test import TestCase
from .models import Report, Impression
# from . import forms
# from . import views
from django.contrib.auth.models import User
from django.test.client import Client


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
        time = '0000'

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
        user_id = 'user'
        user_id2 = 'user2'
        password = '1234'
        null_password = ''

        #ユーザの作成
        new_user = User.objects.create_user(user_id, None, password)
        new_user = User.objects.create_user(user_id2, None, null_password)
        new_user.save()

        #作成したユーザ情報を呼び出し
        saved_user = User.objects.all()
        actual_user = saved_user[0]
        actual_user2 = saved_user[1]

        #作成したユーザのIDとパスワードが一致しているか確認
        #ID、パスワード共に入力されたとき
        self.assertEquals(actual_user.username,user_id)
        self.assertTrue(actual_user.check_password(password))

        #IDは入力され、パスワードが入力されなかったとき
        self.assertEquals(actual_user2.username, user_id2)
        self.assertTrue(actual_user2.check_password(null_password))

    #IDに入力がない場合、ユーザーが作成されないかどうか
    def test_not_make_user(self):
        #設定するIDとパスワード
        true_user_id = 'user'
        true_password = '1234'
        null_user_id = ''
        null_password = ''

        #ユーザの作成
        self.assertRaises(ValueError, lambda: User.objects.create_user(null_user_id, None,null_password))

    #作成したユーザがログインできるかどうか
    def test_login(self):
        #ログインするユーザ情報(ID、パスワード)
        user_id = 'user'
        password = '1234'

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
        password = '1234'

        # ユーザを作成
        new_user = User.objects.create_user(user_id, None, password)
        new_user.save()

        # self.assertIsNotNone(new_user)

        # 作成したユーザに異なるパスワードでログインできないかを確認
        client_user = Client()
        self.assertFalse(client_user.login(username=user_id, password='error_password'))









