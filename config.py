# encoding:utf-8
import os
from datetime import timedelta
SECRET_KEY=os.urandom(24) #每次重启服务器的时候清除session
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI='mysql://root:2569535507Lw@127.0.0.1/COVID' #数据库配置 格式：mysql://账号:密码@127.0.0.1/COVID
PERMANENT_SESSION_LIFETIME=timedelta(days=1) #session有效期为1天
SQLALCHEMY_TRACK_MODIFICATIONS=False
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
MAIL_USERNAME = "zjulw@qq.com"
MAIL_PASSWORD = "nwprbhqdjsvedjdc"  # 生成的授权码
MAIL_DEFAULT_SENDER = "zjulw@qq.com"




