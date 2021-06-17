from django.db import reset_queries
from django.shortcuts import render
from good.models import *
from user.models import *
from trade.models import *
from demand.models import *
from trade.views import *
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
		l = [i.category for i in category]
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
			result = {'result': 0, 'message': '请先登录!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		user = Main.objects.get(ID = id)
		if user.wxid == "":
			result = {'result': 0, 'message': '请先填写微信号后再上传商品!'}
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
def updategood(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		id = int(data_json.get('id'))
		newgood = GoodInfo.objects.get(goodid = id)
		newgood.goodname = data_json.get('name')
		newgood.description = data_json.get('description')
		newgood.categoryid = int(data_json.get('category'))
		newgood.price = float(data_json.get('price'))
		newgood.save()
		result = {'result': 1, 'message': '修改成功!', 'id': newgood.goodid}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getgood(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token', 0)
		id = Check(token)
		if int(data_json.get('id', -1)) != -1:
			id = int(data_json.get('id', -1))
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")

		l = GoodInfo.objects.filter(userid = id)
		id = [i.goodid for i in l]
		name = [i.goodname for i in l]
		description = [i.description for i in l]
		price = [i.price for i in l]
		url = []
		for i in l:
			if GImg.objects.filter(goodid = i.goodid).exists() == True:
				imgs = GImg.objects.filter(goodid = i.goodid)
				url.append(MEDIA_SERVER + imgs[0].img.url)
			else:
				url.append('https://z3.ax1x.com/2021/06/09/2cqBCD.png')
		result = {'result': 1, 'message': '获取成功!', 'id':id, 'name':name, 'description':description, 'price':price, 'url':url}
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

def CanTrade(goodid, id):
	if id == -1:
		return False
	if Trade.objects.filter(objectID = goodid, type = 0, ownID = id).exists():
		return False
	if Trade.objects.filter(objectID = goodid, type = 0, requestID = id).exists():
		return False
	return True

@csrf_exempt
def goodinfo(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		'''
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		'''
		goodid = int(data_json.get('id'))
		result = {}
		Good = GoodInfo.objects.get(goodid = goodid)
		if id == Good.userid:
			result['own'] = True
		else:
			result['own'] = False
		if GoodCollect.objects.filter(userID = id, goodID = Good.goodid).exists():
			result['iscollect'] = True
		else:
			result['iscollect'] = False
		result['userid'] = Good.userid
		result["title"] = Good.goodname
		result["price"] = Good.price
		result["description"] = Good.description
		result["isSold"] = 1 - Good.onsale
		result["date"] = Good.uploadtime[:19]
		result["category"] = Good.categoryid
		if data_json.get('token')==None:
			result["canTrade"] = False
		else:	
			result["canTrade"] = CanTrade(goodid, Check(data_json.get("token")))
		if GImg.objects.filter(goodid = goodid).exists() == True:
			imgs = GImg.objects.filter(goodid = goodid)
			result["imageUrls"] = [(MEDIA_SERVER + i.img.url) for i in imgs]
		else:
			result["imageUrls"] = ["https://z3.ax1x.com/2021/06/09/2cqBCD.png"]
		
		release = UserInfo.objects.get(userID = Good.userid)
		result["name"] = Main.objects.get(ID = Good.userid).username
		result["credit"] = release.score
		if Userheadshot.objects.filter(userID = Good.userid).exists()==True:
			result["avatar"] = MEDIA_SERVER + Userheadshot.objects.get(userID = Good.userid).headshot.url
		else:
			result["avatar"] = "https://z3.ax1x.com/2021/06/09/2cTNY4.png"

		result["result"] = 1
		result["message"] = "查询成功"
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def allgood(request):
	if request.method == 'POST':
		result = {'result': 1, 'message': '获取成功!'}
		all = GoodInfo.objects.all()
		good = []
		for i in all:
			if i.onsale == False:
				continue
			d = {}
			d["id"] = i.goodid
			d["price"] = i.price
			d["name"] = i.goodname
			if GImg.objects.filter(goodid = i.goodid).exists() == True:
				imgs = GImg.objects.filter(goodid = i.goodid)
				d["urls"] = (MEDIA_SERVER + imgs[0].img.url)
			else:
				d["urls"] = "https://z3.ax1x.com/2021/06/09/2cqBCD.png"
			
			good.append(d)
		result["good"] = good
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def search(request):
	if request.method == 'POST':
		result = {'result': 1, 'message': '搜索成功!'}

		data_json = json.loads(request.body)
		type = int(data_json.get('type'))
		print(data_json.get('key'))
		key = str(data_json.get('key'))
		category = int(data_json.get('category'))
		object = []
		if type == 0:
			good = GoodInfo.objects.filter(goodname__icontains = key)
			for i in good:
				if i.onsale == False or (i.categoryid != category and category != 0):
					continue
				d = {'id': i.goodid, 'name': i.goodname, 'type': 0, 'price': i.price}
				if GImg.objects.filter(goodid = i.goodid).exists() == True:
					imgs = GImg.objects.filter(goodid = i.goodid)
					d['urls'] = MEDIA_SERVER + imgs[0].img.url
				else:
					d['urls'] = "https://z3.ax1x.com/2021/06/09/2cqBCD.png"
				object.append(d)
		else:
			demand = DemandInfo.objects.filter(demandname__icontains = key)
			for i in demand:
				if i.onsale == False or (i.categoryid != category and category != 0):
					continue
				d = {'id': i.demandid, 'name': i.demandname, 'type': 0, 'price': i.price}
				if DImg.objects.filter(demandid = i.demandid).exists() == True:
					imgs = DImg.objects.filter(demandid = i.demandid)
					d['urls'] = MEDIA_SERVER + imgs[0].img.url
				else:
					d['urls'] = "https://z3.ax1x.com/2021/06/09/2cqBCD.png"
				object.append(d)
		# Search object by given id
		result['len'] = len(object)
		result['object'] = object
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def report(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		id = int (data_json.get('id'))
		type = int(data_json.get('type'))
		if type == 0:
			Good = GoodInfo.objects.get(goodid = id)
			SendInfo(0, 5, "商品名为" + Good.goodname + "的商品被举报,请及时检查其是否有违规信息", id, -1)
		else:
			Demand = DemandInfo.objects.get(demandid = id)
			SendInfo(0, 5, "需求名为" + Demand.demandname + "的需求被举报,请及时检查其是否有违规信息", -1, id)
		result = {'result': 1, 'message': '举报成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def delete(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		id = int (data_json.get('id'))
		type = int(data_json.get('type'))
		if type == 0:
			Good = GoodInfo.objects.get(goodid = id)
			Good.onsale = False
			Good.save()
			SendInfo(Good.userid, 4, "您的商品"+ Good.demandname+"已下架",
				id, -1)
		else:
			Demand = DemandInfo.objects.get(demandid = id)
			Demand.onsale = False
			Demand.save()
			SendInfo(Demand.userid, 4, "您的需求"+ Demand.demandname+"已下架",
				  -1, id)
		result = {'result': 1, 'message': '下架成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")