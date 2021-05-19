from random import Random  				# 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings		# setting.py添加的的配置信息

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


# 发送电子邮件
def send_code_email(email):
	"""
	发送电子邮件
	:param email: 要发送的邮箱
	:param send_type: 邮箱类型
	:return: True/False
	"""
	# 将给用户发的信息保存在数据库中
	code = random_str(16)
	email_title = ""
	email_body = ""
	# 如果为注册类型
	email_title = "注册激活"
	# email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
	email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
	# 发送邮件
	send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
	if not send_status:
		print('Fail!')
	else:
		print('Success!')