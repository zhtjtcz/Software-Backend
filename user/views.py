from django.shortcuts import render
from user.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.email_send import *
# Create your views here.

@csrf_exempt
def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		email = request.POST.get('email')
		wxid = request.POST.get('wxid')
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
				all = Main.objects.all()
				count = len(all) + 1
				new_user = Main()
				new_user.ID = count
				new_user.username = username
				new_user.password = password1
				new_user.email = email
				new_user.wxid = wxid
				new_user.save()
				result = {'result': 1, 'message': '注册成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
# TODO token
def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if len(username)==0 or len(password)==0:
			result = {'result': 0, 'message': r'用户名与密码不允许为空!'}
		else:
			if Main.objects.filter(username=username).exists() == False:
				result = {'result': 0, 'message': '用户不存在!'}
			else:
				user = Main.objects.get(username=username)
				if user.password != password:
					result = {'result': 0, 'message': '密码不正确!'}
				else:
					result = {'result': 1, 'message': '登录成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def email(request):
	if request.method == 'POST':
		Email = request.POST.get('email')
		send_code_email(Email)