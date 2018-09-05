#-*- codingL:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
mail_host = 'smtp.139.com'
mail_user = '18792146966@139.com'
mail_pass = 'lyb12153719'


msg = MIMEText('The body of email is here!') 
msg['Subject'] = 'An email alert'
msg['From'] = '18792146966@139.com'
msg['To'] = '18256920032@139.com'

smtpObj = smtplib.SMTP()
smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
smtpObj.login(mail_user, mail_pass) #登录邮箱
smtpObj.send_message(msg)
smtpObj.quit
