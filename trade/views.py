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
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		type = int(data_json.get('type'))
		objectID = int(data_json.get('objectID'))
		if type == 0:
			own = GoodInfo.objects.get(goodid = objectID).userid
		else:
			own = DemandInfo.objects.get(demandid = objectID).userid
		
		trade = Trade(ID = len(Trade.objects.all()), objectID = objectID, type =  type,
			requestID = id, ownID = own, status = 0, score = 0.0)
		trade.save()
		# TODO send a info
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

		apply.status = confirm
		# TODO confirm info
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
		objectID = int(data_json.get('objectID'))

		if type == 0:
			own = GoodInfo.objects.get(goodid = objectID)
			if own.userid != id:
				result = {'result': 0, 'message': '权限错误!'}
				return HttpResponse(json.dumps(result), content_type="application/json")
			alltarde = Trade.objects.filter(objectID = objectID, type = type, ownID = id)

		else:
			own = DemandInfo.objects.get(demandid = objectID)
			if own.userid != id:
				result = {'result': 0, 'message': '权限错误!'}
				return HttpResponse(json.dumps(result), content_type="application/json")
			alltarde = Trade.objects.filter(objectID = objectID, type = type, ownID = id)

		apply = []

		for i in alltarde:
			d = {}
			d["name"] = Main.objects.get(ID = i.requestID).username
			d["id"] = i.ID
			apply.append(d)

		result = {'result': 1, 'message': '成功!', "apply" : apply}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")