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
		newdemand = DemandInfo()
		newdemand.demandid = len(DemandInfo.objects.all())
		newdemand.userid = GetID(token)
		newdemand.demandname = data_json.get('name')
		newdemand.description = data_json.get('description')
		newdemand.categoryid = int(data_json.get('category'))
		newdemand.price = float(data_json.get('price'))
		newdemand.uploadtime = str(datetime.datetime.now())
		newdemand.onsale = True
		newdemand.save()
		result = {'result': 1, 'message': '上传成功!', 'id': newdemand.demandid}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def dupload(request):
	if request.method == 'POST':
		source = request.FILES.get('file')
		token = request.META.get('HTTP_AUTHORIZATION')
		if Check(token, request)==False:
			return HttpResponse(json.dumps({'result': 0, 'message': 'Token有误!'}), content_type="application/json")
		demangid = request.META.get('HTTP_ID')
		if source:
			image = DImg(imgid=len(DImg.objects.all()), demangid=demangid, img=source)
			image.save()
			return HttpResponse(json.dumps({'success': True,'path': MEDIA_SERVER + image.img.url, 'url':image.img.url}))
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")