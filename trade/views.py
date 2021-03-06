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
from inform.views import *
import datetime
import traceback
# Create your views here.

@csrf_exempt
def apply(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': '请先登录!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		if Main.objects.get(ID = id).wxid == "":
			result = {'result': 0, 'message': '您还未填写微信号,请填写微信号后再申请交易!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		type = int(data_json.get('type'))
		objectID = int(data_json.get('objectid'))
		if type == 0:
			own = GoodInfo.objects.get(goodid = objectID).userid
			name = GoodInfo.objects.get(goodid = objectID).goodname
		else:
			own = DemandInfo.objects.get(demandid = objectID).userid
			name = DemandInfo.objects.get(demandid = objectID).demandname
		
		if id == own:
			result = {'result': 0, 'message': '不能申请和自己交易!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		
		if Trade.objects.filter(objectID = objectID, type = type,requestID = id, ownID = own).exists() == True:
			result = {'result': 0, 'message': '不能重复申请!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		if BanInfo.objects.filter(userID = id).exists() == True:
			result = {'result': 0, 'message': '您已被封禁,不能申请交易!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		trade = Trade(ID = len(Trade.objects.all()), objectID = objectID, type = type,
			requestID = id, ownID = own, status = 0, score = 0.0)
		trade.save()

		if type == 0:
			goodid,demandid = objectID,-1
		else:
			demandid,goodid = objectID,-1
		SendInfo(own, 1, "有用户申请与您上架的" + name + "进行交易,请到详情页查看并及时确认.",
			goodid, demandid)
		result = {'result': 1, 'message': '申请成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def confirm(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		applyID = int(data_json.get('applyID'))
		apply = Trade.objects.get(ID = applyID)
		if apply.ownID != id:
			result = {'result': 0, 'message': '权限错误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")

		confirm = int(data_json.get('confirm'))

		if apply.type == 0:
			good = GoodInfo.objects.get(goodid = apply.objectID)
			if good.onsale == False:
				result = {'result': 0, 'message': '已进行过交易!'}
				return HttpResponse(json.dumps(result), content_type="application/json")
		else:
			demand = DemandInfo.objects.get(demandid = apply.objectID)
			if demand.onsale == False:
				result = {'result': 0, 'message': '已进行过交易!'}
				return HttpResponse(json.dumps(result), content_type="application/json")

		apply.status = confirm
		if confirm == 1:
			if apply.type == 0:
				good = GoodInfo.objects.get(goodid = apply.objectID)
				good.onsale = False
				good.save()
				SendInfo(apply.requestID, 3, "您的交易请求已被确认,对方微信为"+ Main.objects.get(ID = apply.ownID).wxid +",请尽快完成交易,并在完成后进行评分.",
					apply.objectID, -1, apply.ID)
			else:
				demand = DemandInfo.objects.get(demandid = apply.objectID)
				demand.onsale = False
				demand.save()
				SendInfo(apply.ownID, 3, "交易请求已确认,对方微信为"+ Main.objects.get(ID = apply.requestID).wxid +",请尽快完成交易,并在完成后进行评分.",
					-1, apply.objectID, apply.ID)
		else:
			if apply.type == 0:
				goodid,demandid = apply.objectID,-1
			else:
				demandid,goodid = apply.objectID,-1
			SendInfo(apply.requestID, 2, "您的交易请求已被拒绝.", goodid, demandid)
		apply.save()

		result = {'result': 1, 'message': '成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def applylist(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		type = int(data_json.get('type'))
		objectID = int(data_json.get('objectid'))

		if type == 0:
			own = GoodInfo.objects.get(goodid = objectID)
			if own.userid != id:
				result = {'result': 0, 'message': '权限错误!'}
				return HttpResponse(json.dumps(result), content_type="application/json")
			
			if own.onsale == False:
				result = {'result': 1, 'message': '成功!', "apply": []}
				return HttpResponse(json.dumps(result), content_type="application/json")
			alltarde = Trade.objects.filter(objectID = objectID, type = type, ownID = id)

		else:
			own = DemandInfo.objects.get(demandid = objectID)
			if own.userid != id:
				result = {'result': 0, 'message': '权限错误!'}
				return HttpResponse(json.dumps(result), content_type="application/json")
			if own.onsale == False:
				result = {'result': 1, 'message': '成功!', "apply": []}
				return HttpResponse(json.dumps(result), content_type="application/json")
			alltarde = Trade.objects.filter(objectID = objectID, type = type, ownID = id)

		apply = []

		for i in alltarde:
			if i.status != 0:
				continue
			d = {}
			d["name"] = Main.objects.get(ID = i.requestID).username
			d["userid"] = Main.objects.get(ID = i.requestID).ID
			d["id"] = i.ID
			apply.append(d)

		result = {'result': 1, 'message': '成功!', "apply" : apply}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def tradehistory(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		history = []
		if Trade.objects.filter(type = 0, ownID = id, status = 1).exists() == True:
			trade = Trade.objects.filter(type = 0, ownID = id, status = 1)
			for i in trade:
				d = {"objectid": i.objectID, "type": i.type, "score": i.score}
				history.append(d)
		if Trade.objects.filter(type = 1, requestID = id, status = 1).exists() == True:
			trade = Trade.objects.filter(type = 1, requestID = id, status = 1)
			for i in trade:
				d = {"objectid": i.objectID, "type": i.type, "score": i.score}
				history.append(d)
		if history == []:
			history.append("NULL")
		result = {'result': 1, 'message': '成功!', 'history': history}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")