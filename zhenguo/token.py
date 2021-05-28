from jwt import encode
from jwt import decode
import datetime
from user.models import Main

def GetToken(name):
	time = datetime.datetime.now()
	return encode({'username':name, 'logintime': str(time), 'id':Main.objects.get(username=name)}, 'secret_key', algorithm='HS256')

def Check(token):
	try:
		s = decode(token[1:-1],  'secret_key', algorithm='HS256')
	except:
		return -1
	return s.get('id',-1)