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

@csrf_exempt
def getdemand(request):
	if request.method == 'GET':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)

		l = DemandInfo.objects.filter(userid = id)
		name = [i.demandname for i in l]
		description = [i.description for i in l]
		price = [i.price for i in l]
		url = []
		for i in l:
			if DImg.objects.filter(demandid = i.demandid).exists() == True:
				imgs = DImg.objects.filter(demandid = i.demandid)
				url.append(MEDIA_SERVER + imgs[0].img.url)
			else:
				url.append('NULL')
		result = {'result': 1, 'message': '获取成功!', 'name':name, 'description':description, 'price':price, 'url':url}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def demandcollect(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		demandid = int(data_json.get('demandid'))
		if DemandCollect.objects.filter(userID = id, demandID = demandid).exists() == True:
			result = {'result': 0, 'message': '已收藏该需求!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		NewCollect = DemandCollect(userID = id, demandID = demandid)
		NewCollect.save()
		result = {'result': 1, 'message': '收藏成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def demanduncollect(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		
		if Check(token, request)==False:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		id = GetID(token)
		demandid = int(data_json.get('demandid'))
		if DemandCollect.objects.filter(userID = id, demandID = demandid).exists() == False:
			result = {'result': 0, 'message': '未收藏该需求!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		Collect = DemandCollect.objects.get(userID = id, demandID = demandid)
		Collect.delete()
		result = {'result': 1, 'message': '取消收藏成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")