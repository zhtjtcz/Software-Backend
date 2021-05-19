import jwt

def GetToken(name, time):
	return jwt.encode({'username':name,'logintime':time},'f4-*asd7f45ad5+9tr7+',algorithm='HS256')

def Check(token, request):
	x = request.session.get('token',0)
	if x == 0 or x != token:
		return False
	else:
		return True