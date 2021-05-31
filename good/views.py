from django.shortcuts import render
from good.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GImg
from zhenguo.settings import *
from zhenguo.token import *
import datetime
import traceback
# Create your views here.

@csrf_exempt
def getcategory(request):
	if request.method == 'POST':
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		category = Category.objects.all()
		l = [i.name for i in category]
		result = {'result': 1, 'sum': len(l), 'category': l}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def upload(request):
	if request.method == 'POST':
		source = request.FILES.get('file')
		goodid = int(request.META.get('HTTP_AUTHORIZATION'))
		if source:
			image = GImg(imgid=len(GImg.objects.all()), goodid=goodid, img=source)
			image.save()
			return HttpResponse(json.dumps({'success': True,'path': MEDIA_SERVER + image.img.url, 'url':image.img.url}))
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def creategood(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token','0')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		newgood = GoodInfo()
		newgood.goodid = len(GoodInfo.objects.all())
		newgood.userid = id
		newgood.goodname = data_json.get('name')
		newgood.description = data_json.get('description')
		newgood.categoryid = int(data_json.get('category'))
		newgood.price = float(data_json.get('price'))
		newgood.uploadtime = str(datetime.datetime.now())
		newgood.onsale = True
		newgood.save()
		result = {'result': 1, 'message': '上传成功!', 'id': newgood.goodid}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getgood(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")

		l = GoodInfo.objects.filter(userid = id)
		name = [i.goodname for i in l]
		description = [i.description for i in l]
		price = [i.price for i in l]
		url = []
		for i in l:
			if GImg.objects.filter(goodid = i.goodid).exists() == True:
				imgs = GImg.objects.filter(goodid = i.goodid)
				url.append(MEDIA_SERVER + imgs[0].img.url)
			else:
				url.append('NULL')
		result = {'result': 1, 'message': '获取成功!', 'name':name, 'description':description, 'price':price, 'url':url}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def goodcollect(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		goodid = int(data_json.get('goodid'))
		if GoodCollect.objects.filter(userID = id, goodID = goodid).exists() == True:
			result = {'result': 0, 'message': '已收藏该商品!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		NewCollect = GoodCollect(userID = id, goodID = goodid)
		NewCollect.save()
		result = {'result': 1, 'message': '收藏成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def gooduncollect(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		goodid = int(data_json.get('goodid'))
		if GoodCollect.objects.filter(userID = id, goodID = goodid).exists() == False:
			result = {'result': 0, 'message': '未收藏该商品!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		Collect = GoodCollect.objects.get(userID = id, goodID = goodid)
		Collect.delete()
		result = {'result': 1, 'message': '取消收藏成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")