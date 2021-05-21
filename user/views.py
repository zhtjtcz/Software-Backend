from django.shortcuts import render
from user.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.email_send import *
from zhenguo.token import *
# Create your views here.

@csrf_exempt
def register(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		username = data_json.get('username')
		password1 = data_json.get('password1')
		password2 = data_json.get('password2')
		email = data_json.get('email')
		code = data_json.get('code')

		if Main.objects.filter(username=username).exists():
			result = {'result': 0, 'message': '用户已存在!'}
		elif Main.objects.filter(email=email).exists():
			result = {'result': 0, 'message': '邮箱已注册!'}
		elif password1 != password2:
			result = {'result': 0, 'message': '两次密码不匹配!'}
		else:
			name,edu = email.split('@')
			if edu != 'buaa.edu.cn':
				result = {'result': 0, 'message': '邮箱格式不正确!'}
			else:
				if CheckCode(code)==False:
					result = {'result': 0, 'message': '邮箱验证码错误!'}
					return  HttpResponse(json.dumps(result), content_type="application/json")
				all = Main.objects.all()
				count = len(all)
				new_user = Main(ID=count, username=username, password=password1, email=email)
				new_user.save()
				result = {'result': 1, 'message': '注册成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def login(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		username = data_json.get('username')
		password = data_json.get('password')
		
		if len(username)==0 or len(password)==0:
			result = {'result': 0, 'message': '用户名与密码不允许为空!'}
		else:
			if Main.objects.filter(username=username).exists() == False:
				result = {'result': 0, 'message': '用户不存在!'}
			else:
				user = Main.objects.get(username=username)
				if user.password != password:
					result = {'result': 0, 'message': '密码不正确!'}
				else:
					request.session['username'] = username
					token = GetToken(username)
					token = str(token)
					token = token[1:]
					request.session['token'] = token
					result = {'result': 1, 'message': '登录成功!', 'token': token}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def email(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		Email = data_json.get('email')
		name,edu = Email.split('@')
		if edu != 'buaa.edu.cn' or Email.count('@')!=1:
			result = {'result': 0, 'message': '邮箱格式不正确!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		else:
			send_result = SendCodeEmail(Email)
			if send_result == False:
				result = {'result': 0, 'message': '发送失败!请检查邮箱格式'}
			else:
				result = {'result': 1, 'message': '发送成功!请及时在邮箱中查收.'}
			return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def logout(request):
	request.session.flush()