# ����A�v���h�L�������g

# �����
windows7(32bit)  
python3.5.1  
PostgreSQL9.5.3(32bit)  

# �f�[�^�x�[�X�̍쐬
1. PostgreSQL�Ƀ��O�C��  
psql postgres postgres  
�p�X���[�h���͉�ʂ��\�������̂ŁA�ݒ肵���p�X���[�h�����

1. ���O�C����Ƀ��[�U�[�̍쐬�A�p�X���[�h�̕t�^�A�f�[�^�x�[�X�̍쐬���s��  
create user '���[�U�[��';  
alter role ���[�U�[�� with password '�p�X���[�h';  
create database '�f�[�^�x�[�X��' owner '���[�U�[��';  

1. database.dummy.py�ɐݒ肵���f�[�^�x�[�X���A���[�U���A�p�X���[�h����͂��A�t�@�C������dummy�������폜����  
database.dummy.py  
name = "�f�[�^�x�[�X��"  
user = ""���[�U��  
password = "�p�X���[�h"  
host = "localhost"  
port = ""  

# ����A�v���̎��s
1. �f�[�^�x�[�X��makemigrations  
web_application_nippo/daily_report�̃f�B���N�g���Ɉړ�  
�R�}���h���s  
python manage.py makemigrations  

1. ����migrate(�����f�B���N�g����)  
python manage.py migrate

1. runserver�œ���A�v�������s  
python manage.py runserver

1. �u���E�U��œ���A�v���𓮂���  
http://127.0.0.1:8000/�Ƒłƃ��O�C����ʂɑJ��


