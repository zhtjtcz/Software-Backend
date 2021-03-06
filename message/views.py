from django.shortcuts import render
from demand.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zhenguo.settings import *
from zhenguo.token import *
from message.models import *
from user.models import *
from inform.views import *
import datetime
import traceback
# Create your views here.

@csrf_exempt
def reply(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		msg = Msg(ID=len(Msg.objects.all()), objectID=int(data_json.get('objectid')), type=int(data_json.get('type')),
			sendID=id, replyID=int(data_json.get('reply')), text=data_json.get('text'), sendtime=str(datetime.datetime.now()))
		msg.save()
		if int(data_json.get('reply')) != -1:
			msg2 = Msg.objects.get(ID = msg.replyID)
			user = Main.objects.get(ID = msg2.sendID)
			if int(data_json.get('type')) == 0:
				goodid,demandid = msg.objectID,-1
			else:
				demandid,goodid = msg.objectID,-1
			SendInfo(user.ID, 0, "你的留言有了一个新的回复，请点此查看详情", goodid = goodid, demandid = demandid)
			pass
		
		result = {'result': 1, 'message': '留言成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")

def GetReplyInfo(i):
	d = {"text":i.text, "sendtime":i.sendtime[:16]}
	d["username"] = Main.objects.get(ID = i.sendID).username
	d["userid"] = i.sendID
	if Userheadshot.objects.filter(userID = i.sendID).exists() == False:
		d['url'] = 'https://z3.ax1x.com/2021/06/09/2cTNY4.png'
	else:
		d["url"] = MEDIA_SERVER + Userheadshot.objects.get(userID = i.sendID).headshot.url

	d["id"] = i.ID
	return d

@csrf_exempt
def getreply(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		objectID = data_json.get('objectid')
		Type = data_json.get('type')

		if Msg.objects.filter(objectID = objectID, type = Type).exists() == False:
			result = {'result': 1, 'message': '暂无评论', 'reply':"NULL"}
			return HttpResponse(json.dumps(result), content_type="application/json")
		ans = []
		all = Msg.objects.filter(objectID = objectID, type = Type)
		deep = [i for i in all if i.replyID==-1]
		reply = [i for i in all if i.replyID!=-1]
		deep =  sorted(deep, key = lambda x:x.sendtime)
		reply = sorted(reply, key = lambda x:x.sendtime)
		for i in deep:
			d = GetReplyInfo(i)
			d["subreply"] =  [GetReplyInfo(j) for j in reply if j.replyID == i.ID]
			ans.append(d)
		
		result = {'result': 1, 'message': '查询成功', 'reply': ans}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")