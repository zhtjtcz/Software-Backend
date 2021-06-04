from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zhenguo.settings import *
from zhenguo.token import *
from message.models import *
from user.models import *
from trade.models import *
from demand.models import *
from good.models import *
from inform.models import *
import datetime
import traceback
# Create your views here.

def SendInfo(userid, type, text):
	ID = len(Inform.objects.all())
	inform = Inform(ID = ID, type = type, text = text, userid = userid, isread = False, score = False)
	inform.save()

@csrf_exempt
def Infolist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")

		trans = ["留言回复通知", "交易申请通知", "交易完成通知", "商品封禁通知"]
		ans = []
		
		if Inform.objects.filter(userid = id).exists() == False:
			result = {'result': 1, 'message': '获取成功!', "inform":["NULL"]}
		else:
			inform = Inform.objects.filter(userid = id).exists()
			for i in inform:
				d = {"id":i.ID, "name":trans[i.type], "isread":i.isread}
				ans.append(d)
		
		result = {'result': 1, 'message': '获取成功!', "inform": ans}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def Infolist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")

		trans = ["留言回复通知", "交易申请通知", "交易完成通知", "商品封禁通知"]
		informid = int(data_json.get('infoid'))
		inform = Inform.objects.get(ID = informid)
		inform.isread = True
		result = {'result': 1, 'message': '获取成功!', "id": informid, "title": trans[inform.type], 
			"text": inform.texts, "score": inform.score}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")