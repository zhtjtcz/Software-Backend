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
from user.views import *
import datetime
import traceback
# Create your views here.

trans = ["留言回复通知", "交易申请通知", "申请拒绝通知", "申请通过通知", "商品封禁通知", "商品举报通知"]

def SendInfo(userid, type, text, goodid, demandid, Id = -1):
	ID = len(Informs.objects.all())
	inform = Informs(ID = ID, type = type, text = text, userid = userid, isread = False, score = False,
	  date = str(datetime.datetime.now()), goodid = goodid, demandid = demandid, name = trans[type])
	inform.save()

	if Id != -1:
		score = Score(applyid = Id, informid = inform.ID)
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

		ans = []
		
		if Informs.objects.filter(userid = id).exists() == False:
			result = {'result': 1, 'message': '获取成功!', "inform":["NULL"]}
		else:
			inform = Informs.objects.filter(userid = id)
			for i in inform:
				d = {"id":i.ID, "name":trans[i.type], "isread":i.isread, "time":i.date[:16]}
				ans.append(d)
		ans = sorted(ans, key = lambda x:x["id"])
		ans.reverse()
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
		info = Informs.objects.get(ID = id)
		info.isread = True
		info.save()
		
		result = {'result': 1, 'message': '获取成功!', 'name': info.name, 'text': info.text, 
			'score': info.score, 'objectid': max(info.goodid, info.demandid),
			'time': info.date[:16], 'id': info.ID}
		if info.goodid > info.demandid:
			result['type'] = 0
		else:
			result['type'] = 1
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
		info = Informs.objects.get(ID = infoid)
		info.score = True
		info.save()
		score = Score.objects.get(informid = infoid)
		apply = Trade.objects.get(ID = score.applyid)
		apply.score = s
		apply.save()
		Update(apply.ownID)
		Update(apply.requestID)
		result = {'result': 1, 'message': '成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")