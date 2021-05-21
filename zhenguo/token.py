from jwt import encode
import datetime

def GetToken(name):
	time = datetime.datetime.now()
	return encode({'username':name,'logintime': str(time)}, 'secret_key', algorithm='HS256')

def Check(token, request):
	x = request.session.get('token',0)
	if x == 0 or x != token:
		return False
	else:
		return True