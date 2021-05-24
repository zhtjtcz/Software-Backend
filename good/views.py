from django.shortcuts import render
from good.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GoodImg
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
		head = request.META.get('HTTP_AUTHORIZATION')
		if source:
			image = GoodImg(imgid=len(GoodImg.objects.all()), img=source)
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
		if Check(token, request)==False:
			return HttpResponse(json.dumps({'result': 0, 'message': 'Token有误!'}), content_type="application/json")
		newgood = GoodInfo()
		newgood.goodid = len(GoodInfo.objects.all())
		newgood.userid = GetID(token)
		newgood.goodname = data_json.get('name')
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

