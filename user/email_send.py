from random import Random  				# 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings		# setting.py添加的的配置信息
from user.models import *

import datetime

# 生成随机字符串
def random_str(randomlength=8):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str

def SendCodeEmail(email):
	code = random_str(16)
	NewCode = EmailCode()
	NewCode.code = code
	NewCode.save()

	email_title = "榛果交易平台注册激活验证码"
	email_body = "欢迎您注册榛果交易平台!\n"
	email_body += "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证.\n".format(code)
	email_body += "如果您从未注册过榛果交易平台,请忽略该邮件."

	send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
	return send_status

def CheckCode(code):
	if EmailCode.objects.filter(code=code).exists() == False:
		return False
	else:
		EmailCode.objects.filter(code=code).delete()
		return True