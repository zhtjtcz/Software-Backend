from jwt import encode
from jwt import decode
import datetime
from user.models import Main

def GetToken(name, level):
	time = datetime.datetime.now()
	return encode({'username':name, 'logintime': str(time), 'id':Main.objects.get(username=name).ID, 'level':level
		}, 'secret_key', algorithm='HS256')

def Check(token):
	try:
		s = decode(token[1:-1],  'secret_key', algorithm='HS256')
	except:
		return -1
	return s.get('id',-1)

def TokenLevel(token):
	try:
		s = decode(token[1:-1],  'secret_key', algorithm='HS256')
	except:
		return -1
	return s.get('level',-998244353)
