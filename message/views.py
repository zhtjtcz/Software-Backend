from django.shortcuts import render
from demand.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from zhenguo.settings import *
from zhenguo.token import *
from message.models import *
import datetime
import traceback
# Create your views here.

@csrf_exempt
def uploadinfo(request):
	if request.method == 'POST':
		data_json = json.loads(request.body)
		token = data_json.get('token')
		id = Check(token)
		if id==-1:
			result = {'result': 0, 'message': 'Token有误!'}
			return HttpResponse(json.dumps(result), content_type="application/json")
		msg = Msg(ID=len(Msg.objects.all()), objectID=data_json.get('objectid'), type=data_json.get('type'),
			sendID=id, replyID=data_json.get('reply'), text=data_json.get('text'), sengtime=str(datetime.datetime.now()))
		msg.save()
		result = {'result': 1, 'message': '留言成功!'}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'result': 0, 'message': '前端炸了!'}
		return HttpResponse(json.dumps(result), content_type="application/json")