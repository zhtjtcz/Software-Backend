from django.shortcuts import render
from user.models import *
from good.models import *
from demand.models import *
from trade.models import *
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
				new_info = UserInfo(userID = count, score = 5.0)
				new_info.save()
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
					result = {'result': 1, 'message': '登录成功!', 'level': 1}
					if user.ID == 0:
						result['level'] = -1
					# Is Administrator
					elif BanInfo.objects.filter(userID = user.ID).exists() == True:
						result['level'] = 0
					# User has been banned
					token = GetToken(username, result['level'])
					token = str(token)
					token = token[1:]
					request.session['token'] = token
					result['token'] = token
					result['id'] = user.ID
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
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		source = request.FILES.get('file')
		if source:
			if Userheadshot.objects.filter(userID =id).exists() == True:
				image = Userheadshot.objects.get(userID = id)
				image.headshot = source
				image.save()
			else:
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

def Update(id):
	User = UserInfo.objects.get(userID = id)
	sell = Trade.objects.filter(type = 0, ownID = id)
	Sell = Trade.objects.filter(type = 1, requestID = id)
	ans = 0
	cnt = 0
	for i in sell:
		if i.score !=0:
			ans+=i.score
			cnt+=1
	for i in Sell:
		if i.score !=0:
			ans+=i.score
			cnt+=1
	if cnt < 1:
		User.score = 5.0
		User.save()
	else:
		s = "%.2f"%(ans/cnt)
		User.score = s
		User.save()
# Update a user's score

@csrf_exempt
def getuser(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token', -1)
		print(token, Check(token))
		Id = int(data_json.get('id', -1))
		if Id != -1:
			id = Id
		else:
			id = Check(token)
		print(id)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		Update(id)
		base = Main.objects.get(ID = id)
		more = UserInfo.objects.get(userID = id)
		result = {'result': 1, 'message': '查询成功!', 'name': base.username, 'id':id,
			'url': 'https://z3.ax1x.com/2021/06/09/2cTNY4.png', 'score': more.score}
		if Userheadshot.objects.filter(userID = id).exists()==True:
			result['url']=MEDIA_SERVER + Userheadshot.objects.get(userID = id).headshot.url
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def uploadinfo(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		user = UserInfo.objects.get(userID = id)
		user.sex = int(data_json.get('sex'))
		user.grade = int(data_json.get('grade'))
		user.location = int(data_json.get('location'))
		user.telephone = data_json.get('telephone')
		user.save()
		user = Main.objects.get(ID = id)
		user.wxid = data_json.get('wxid')
		user.save()
		result = {'result': 1, 'message': '修改成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")	

@csrf_exempt
def getinfo(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token', 0)
		id = Check(token)
		if int(data_json.get('id', -10)) != -1:
			Id = int(data_json.get('id', -10))
		
		'''
		token = -1, Id = -1		-> Error
		token = -1, Id != -1	-> Other
		token = Id > 0			-> Self
		token > 0, Id = -1		-> Self
		Id = -10				-> Self
		'''
		print(id, Id)
		if (id==-1 and Id==-10) or (id==-1 and Id==-1):
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		if Id == -10 or (id > 0 and Id == -1) or id == Id:
			Update(id)
			base = Main.objects.get(ID = id)
			more = UserInfo.objects.get(userID = id)
			result = {'result': 1, 'message': '查询成功!', 'name': base.username, 'email': base.email, 'wxid': base.wxid,
				'sex': more.sex, 'grade': more.grade, 'telephone': more.telephone, 'location': more.location}
			result['self'] = True
			if base.wxid=="":
				result['wxid'] = -1
			return HttpResponse(json.dumps(result), content_type="application/json")
		else:
			id = Id
			Update(id)
			base = Main.objects.get(ID = id)
			more = UserInfo.objects.get(userID = id)
			result = {'result': 1, 'message': '查询成功!', 'name': base.username, 'email': base.email, 'wxid': base.wxid,
				'sex': more.sex, 'grade': more.grade, 'telephone': more.telephone, 'location': more.location}
			result['self'] = False
			if base.wxid=="":
				result['wxid'] = -1
			return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def follow(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
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
def unfollow(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
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
def followlist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		followlist = UserFollow.objects.filter(userID = id)
		personlist = [UserInfo.objects.get(userID = i.followID) for i in followlist]
		
		Id = [i.userID for i in personlist]
		name = [Main.objects.get(ID = i.userID).username for i in personlist]
		grade = [i.grade if i.grade else -1 for i in personlist]
		location = [i.location if i.location else -1 for i in personlist]
		score = [i.score if i.score else -1 for i in personlist]
		url = []
		for i in personlist:
			if Userheadshot.objects.filter(userID = i.userID).exists() == True:
				imgs = Userheadshot.objects.get(userID = i.userID)
				url.append(MEDIA_SERVER + imgs.headshot.url)
			else:
				url.append('https://z3.ax1x.com/2021/06/09/2cTNY4.png')
		result = {'result': 1, 'message': '获取成功!', 'name': name, 'grade': grade,
			'location': location, 'url':url, 'score': score, 'id': Id}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def goodcollectlist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		
		l = GoodCollect.objects.filter(userID = id)
		l = [GoodInfo.objects.get(goodid = i.goodID) for i in l]
		id = [i.goodid for i in l]
		name = [i.goodname for i in l]
		description = [i.description for i in l]
		price = [i.price for i in l]
		url = []
		for i in l:
			if GImg.objects.filter(goodid = i.goodid).exists() == True:
				imgs = GImg.objects.filter(goodid = i.goodid)
				url.append(MEDIA_SERVER + imgs[0].img.url)
			else:
				url.append('https://z3.ax1x.com/2021/06/09/2cqBCD.png')
		result = {'result': 1, 'message': '获取成功!', 'id':id, 'name':name, 'description':description, 'price':price, 'url':url}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def demandcollectlist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		
		l = DemandCollect.objects.filter(userID = id)
		l = [DemandInfo.objects.get(demandid = i.demandID) for i in l]
		id = [i.demandid for i in l]
		name = [i.demandname for i in l]
		description = [i.description for i in l]
		price = [i.price for i in l]
		url = []
		for i in l:
			if DImg.objects.filter(demandid = i.demandid).exists() == True:
				imgs = DImg.objects.filter(demandid = i.demandid)
				url.append(MEDIA_SERVER + imgs[0].img.url)
			else:
				url.append('https://z3.ax1x.com/2021/06/09/2cqBCD.png')
		result = {'result': 1, 'message': '获取成功!', 'id':id, 'name':name, 'description':description, 'price':price, 'url':url}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def ban(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		banid = int(data_json.get('id'))
		if BanInfo.objects.filter(userID = banid).exists():
			ban = BanInfo.objects.filter(userID = banid)
			ban.delete()
		else:
			ban = BanInfo(userID = banid)
			ban.save()
		result = {'result': 1, 'message': '成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getlevel(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		level = TokenLevel(token)
		result = {'result': 1, 'message': '成功!', 'level':level}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def isban(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		id = int(data_json.get('id'))
		if BanInfo.objects.filter(userID = id).exists() == True:
			result = {'result': 1, 'message': '成功!', 'isban':True}
		else:
			result = {'result': 1, 'message': '成功!', 'isban':False}

		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def changepassword(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		username = data_json.get('username', 'null')
		status = int(data_json.get('status'))
		if username != 'null':
			user = Main.objects.get(username = username)
			if status == 0:
				SendPasswordCodeEmail(user.email)
				result = {'result': 1, 'message': '发送成功!'}
				return HttpResponse(json.dumps(result), content_type="application/json")
			else:
				code = data_json.get('code')
				if EmailCode.objects.filter(code=code).exists() == False:
					result = {'result': 0, 'message': '验证码错误!'}
					return HttpResponse(json.dumps(result), content_type="application/json")
				Code = EmailCode.objects.get(code = code)
				Code.delete()
				password = data_json.get('password')
				user.password = password
				user.save()
				result = {'result': 1, 'message': '修改成功!'}
				return HttpResponse(json.dumps(result), content_type="application/json")

		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		
		user = Main.objects.get(ID = id)
		if status == 0:
			send_result = SendPasswordCodeEmail(user.email)
			print(send_result)
			result = {'result': 1, 'message': '发送成功!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		else:
			code = data_json.get('code')
			if EmailCode.objects.filter(code=code).exists() == False:
				result = {'result': 0, 'message': '验证码错误!'}
				return HttpResponse(json.dumps(result), content_type="application/json")
			Code = EmailCode.objects.get(code = code)
			Code.delete()
			password = data_json.get('password')
			user.password = password
			user.save()
			result = {'result': 1, 'message': '修改成功!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def count(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		id = int(data_json.get('id'))
		result = {'result': 1, 'message': '成功!'}
		result['good'] = len(GoodInfo.objects.filter(userid = id))
		result['demand'] = len(DemandInfo.objects.filter(userid = id))
		result['trade'] = len(Trade.objects.filter(ownID = id, status = 1)) + len(Trade.objects.filter(requestID = id, status = 1))
		result['following'] = len(UserFollow.objects.filter(userID = id))
		result['followed'] = len(UserFollow.objects.filter(followID = id))
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def isfollow(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		Id = int(data_json.get('id'))
		if UserFollow.objects.filter(userID = id, followID = Id).exists():
			result = {'result': 1, 'message': '成功!', 'isfollow': True}
			return HttpResponse(json.dumps(result), content_type="application/json")
		else:
			result = {'result': 1, 'message': '成功!', 'isfollow': False}
			return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

