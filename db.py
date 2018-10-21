# 这个文件的存在是为了避免循环引用的错误

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
