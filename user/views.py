from django.shortcuts import render
from user.models import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username == 'aaa' and password == '111':
			result = {'info': 1}
		else:
			result = {'info': -1}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		result = {'info': -1}
		return HttpResponse(json.dumps(result), content_type="application/json")