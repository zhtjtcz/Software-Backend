from jwt import encode
from jwt import decode
import datetime
from user.models import Main

def GetToken(name):
	time = datetime.datetime.now()
	return encode({'username':name,'logintime': str(time)}, 'secret_key', algorithm='HS256')

def Check(token, request):
	x = request.session.get('token',0)
	if x == 0 or x != token:
		return False
	else:
		return True

def GetID(token):
	s = decode(token[1:-1],  'secret_key', algorithm='HS256')
	user = Main.objects.get(username=s['username'])
	return user.ID
	# maybe change