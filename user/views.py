from good.models import *
from django.shortcuts import render
from user.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.email_send import *
from zhenguo.token import *
from zhenguo.settings import *
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
		#elif Main.objects.filter(email=email).exists():
		#	result = {'result': 0, 'message': '邮箱已注册!'}
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
		if Email.count('@')==1:
			name,edu = Email.split('@')
			if edu == 'buaa.edu.cn':
				send_result = SendCodeEmail(Email)
				if send_result == False:
					result = {'result': 0, 'message': '发送失败!请检查邮箱格式'}
				else:
					result = {'result': 1, 'message': '发送成功!请及时在邮箱中查收.'}
					return HttpResponse(json.dumps(result), content_type="application/json")
			else:
				result = {'result': 0, 'message': '邮箱格式不正确!'}
				return HttpResponse(json.dumps(result), content_type="application/json")	
		else:
			result = {'result': 0, 'message': '邮箱格式不正确!'}
			return HttpResponse(json.dumps(result), content_type="application/json")

	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def logout(request):
	request.session.flush()

@csrf_exempt
def uploadimg(request):
	if request.method == 'POST':
		token = request.META.get('HTTP_AUTHORIZATION', 0)
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		source = request.FILES.get('file')
		if source:
			id = GetID(token)
			image = Userheadshot(userID=id, headshot=source)
			image.save()
			result = {'result': 1, 'id': id,'path': MEDIA_SERVER + image.headshot.url, 'url':image.headshot.url}
			return HttpResponse(json.dumps(result), content_type="application/json")
		else:
			result = {'result': 0, 'message': '请检查上传内容!'}
			return HttpResponse(json.dumps(result), content_type="application/json")	
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def uploadinfo(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		user = UserInfo.objects.get(userID = id)
		user.sex = int(data_json.get('sex'))
		user.grade = int(data_json.get('grade'))
		user.location = int(data_json.get('location'))
		user.telephone = data_json.get('telephone')
		user.save()
		result = {'result': 1, 'message': '修改成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")	

@csrf_exempt
def getinfo(request):
	if request.method == 'GET':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		base = Main.objects.get(ID = id)
		more = UserInfo.objects.get(userID = id)
		result = {'result': 0, 'message': '查询成功!', 'name': base.username, 'email': base.email, 'wxid': base.wxid,
			'sex': more.sex, 'grade': more.grade, 'telephone': more.telephone, 'location': more.location, 'score': more.score}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def follow(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		followingid = Main.objects.get(username=data_json.get('username')).ID
		if UserFollow.objects.filter(userID = id, followID = followingid).exists() == True:
			result = {'result': 0, 'message': '已关注该用户!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		NewFollow = UserFollow(userID = id, followID = followingid)
		NewFollow.save()
		result = {'result': 1, 'message': '关注成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def collect(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		goodid = int(data_json.get('goodid'))
		if UserCollect.objects.filter(userID = id, goodID = goodid).exists() == True:
			result = {'result': 0, 'message': '已收藏该商品!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		NewCollect = UserCollect(userID = id, goodID = goodid)
		NewCollect.save()
		result = {'result': 1, 'message': '收藏成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def unfollow(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		followingid = Main.objects.get(username=data_json.get('username')).ID
		if UserFollow.objects.filter(userID = id, followID = followingid).exists() == False:
			result = {'result': 0, 'message': '未关注该用户!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		Follow = UserFollow.objects.get(userID = id, followID = followingid)
		Follow.delete()
		result = {'result': 1, 'message': '取消关注成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def uncollect(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		goodid = int(data_json.get('goodid'))
		if UserCollect.objects.filter(userID = id, goodID = goodid).exists() == False:
			result = {'result': 0, 'message': '未收藏该商品!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		Collect = UserCollect.objects.get(userID = id, goodID = goodid)
		Collect.delete()
		result = {'result': 1, 'message': '取消收藏成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def followlist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		#TODO follow list
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def collectlist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		
		l = UserCollect.objects.filter(userID = id)
		l = [GoodInfo.objects.get(goodid = i.goodID) for i in l]
		name = [i.goodname for i in l]
		description = [i.description for i in l]
		price = [i.price for i in l]
		url = []
		for i in l:
			if GImg.objects.filter(goodid = i.goodid).exists() == True:
				imgs = GImg.objects.filter(goodid = i.goodid)
				url.append(MEDIA_SERVER + imgs[0].img.url)
			else:
				url.append('NULL')
		result = {'result': 1, 'message': '获取成功!', 'name':name, 'description':description, 'price':price, 'url':url}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")