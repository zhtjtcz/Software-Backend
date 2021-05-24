from django.shortcuts import render
from demand.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zhenguo.settings import *
from zhenguo.token import *
import datetime
import traceback
# Create your views here.

@csrf_exempt
def createdemand(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token','0')
		if Check(token, request)==False:
			return HttpResponse(json.dumps({'result': 0, 'message': 'Token有误!'}), content_type="application/json")
		newgood = DemandInfo()
		newgood.demandid = len(DemandInfo.objects.all())
		newgood.userid = GetID(token)
		newgood.demandname = data_json.get('name')
		newgood.description = data_json.get('description')
		newgood.categoryid = int(data_json.get('category'))
		newgood.price = float(data_json.get('price'))
		newgood.uploadtime = str(datetime.datetime.now())
		newgood.onsale = True
		newgood.save()
		result = {'result': 1, 'message': '上传成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")