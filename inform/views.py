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

def SendInfo(userid, type, text, ID = -1):
	ID = len(Inform.objects.all())
	inform = Inform(ID = ID, type = type, text = text, userid = userid, isread = False, score = False)
	inform.save()
	if ID != -1:
		score = Score(applyid = ID, informid = inform.ID)
		score.save()

@csrf_exempt
def infolist(request):
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
def info(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		id = int(data_json.get('id'))
		info = Inform.objects.get(ID = id)
		trans = ["留言回复通知", "交易申请通知", "交易完成通知", "商品封禁通知"]
		
		result = {'result': 1, 'message': '获取成功!', "name": trans[info.type], "text": info.texts, 
			"type":info.type, 'score': info.score}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def makescore(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		infoid = int(data_json.get('infoid'))
		s = float(data_json.get('score'))
		info = Inform.objects.get(ID = infoid)
		info.score = True
		info.save()
		score = Score.objects.get(informid = infoid)
		apply = Trade.objects.get(ID = score.applyid)
		apply.score = s
		apply.save()

		result = {'result': 1, 'message': '成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")