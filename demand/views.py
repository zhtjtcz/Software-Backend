from django.shortcuts import render
from demand.models import *
from user.models import *
from trade.models import *
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
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		newdemand = DemandInfo()
		newdemand.demandid = len(DemandInfo.objects.all())
		newdemand.userid = id
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
		demandid = int(request.META.get('HTTP_AUTHORIZATION'))
		if source:
			image = DImg(imgid=len(DImg.objects.all()), demandid=demandid, img=source)
			image.save()
			return HttpResponse(json.dumps({'success': True,'path': MEDIA_SERVER + image.img.url, 'url':image.img.url}))
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getdemand(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if int(data_json.get('id', -1)) != -1:
			id = int(data_json.get('id', -1))
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")

		l = DemandInfo.objects.filter(userid = id)
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
		result = {'result': 1, 'message': '获取成功!', 'name':name, 'description':description, 'price':price, 'url':url, 'id':id}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def demandcollect(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
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
		
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
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

def CanTrade(demandid, id):
	if id == -1:
		return False
	if Trade.objects.filter(objectID = demandid, type = 1, ownID = id).exists():
		return False
	if Trade.objects.filter(objectID = demandid, type = 1, requestID = id).exists():
		return False
	return True

@csrf_exempt
def demandinfo(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		demandid = int(data_json.get('id'))
		result = {}
		Demand = DemandInfo.objects.get(demandid = demandid)
		result["title"] = Demand.demandname
		result["price"] = Demand.price
		result["description"] = Demand.description
		result["isSold"] = 1 - Demand.onsale
		result["date"] = Demand.uploadtime[:19]
		if data_json.get('token')==None:
			result["canTrade"] = False
		else:	
			result["canTrade"] = CanTrade(demandid, Check(data_json.get("token")))
		if DImg.objects.filter(demandid = demandid).exists() == True:
			imgs = DImg.objects.filter(demandid = demandid)
			result["imageUrls"] = [(MEDIA_SERVER + i.img.url) for i in imgs]
		else:
			result["imageUrls"] = ["https://z3.ax1x.com/2021/06/09/2cqBCD.png"]
		
		release = UserInfo.objects.get(userID = Demand.userid)
		result["name"] = Main.objects.get(ID = Demand.userid).username
		result["credit"] = release.score
		if Userheadshot.objects.filter(userID = Demand.userid).exists()==True:
			result["avatar"] = MEDIA_SERVER + Userheadshot.objects.get(userID = Demand.userid).headshot.url
		else:
			result["avatar"] = "https://z3.ax1x.com/2021/06/09/2cTNY4.png"

		result["result"] = 1
		result["message"] = "查询成功"
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def alldemand(request):
	if request.method == 'POST':
		result = {'result': 1, 'message': '获取成功!'}
		all = DemandInfo.objects.all()
		demand = []
		for i in all:
			d = {}
			d["id"] = i.demandid
			d["price"] = i.price
			d["name"] = i.demandname
			if DImg.objects.filter(demandid = i.demandid).exists() == True:
				imgs = DImg.objects.filter(demandid = i.demandid)
				d["urls"] = (MEDIA_SERVER + imgs[0].img.url)
			else:
				d["urls"] = "https://z3.ax1x.com/2021/06/09/2cqBCD.png"

			demand.append(d)
		result["demand"] = demand
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")