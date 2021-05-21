from django.shortcuts import render
from good.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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