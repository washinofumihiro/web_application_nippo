# 日報アプリドキュメント

# 動作環境
windows7(32bit)  
python3.5.1  
PostgreSQL9.5.3(32bit)  

# データベースの作成
1. PostgreSQLにログイン  
psql postgres postgres  
パスワード入力画面が表示されるので、設定したパスワードを入力

1. ログイン後にユーザーの作成、パスワードの付与、データベースの作成を行う  
create user 'ユーザー名';  
alter role ユーザー名 with password 'パスワード';  
create database 'データベース名' owner 'ユーザー名';  

1. database.dummy.pyに設定したデータベース名、ユーザ名、パスワードを入力し、ファイル名のdummy部分を削除する  
database.dummy.py  
name = "データベース名"  
user = ""ユーザ名  
password = "パスワード"  
host = "localhost"  
port = ""  

# 日報アプリの実行
1. データベースのmakemigrations  
web_application_nippo/daily_reportのディレクトリに移動  
コマンド実行  
python manage.py makemigrations  

1. 次はmigrate(同じディレクトリで)  
python manage.py migrate

1. runserverで日報アプリを実行  
python manage.py runserver

1. ブラウザ上で日報アプリを動かす  
http://127.0.0.1:8000/と打つとログイン画面に遷移


