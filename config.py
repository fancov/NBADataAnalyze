import os

SECRET_KEY = 'NBANBANBANBANBANBANBANBA'

mysql_username = 'root'
mysql_password = 'root'

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@127.0.0.1:3306/nba?charset=utf8" % (mysql_username, mysql_password)

SQLALCHEMY_COMMIT_ON_TEARDOWN = True

SQLALCHEMY_TRACK_MODIFICATIONS = False


MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USERNAME = 'catyynet@163.com'
MAIL_PASSWORD = os.environ.get('MAIL_PWD')