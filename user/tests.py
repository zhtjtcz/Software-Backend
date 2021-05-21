from django.test import TestCase
import requests
import pandas
import openpyxl
import jwt
import json

# res = requests.post('http://123.57.194.168:8000/login/', data={'username':'AAA', 'password':'111'})
'''
res = requests.post('http://127.0.0.1:8000/email/', data={'email':'18377221@buaa.edu.cn', 'password':'123456'})
print(res.text)
'''

result = {'result': 1, 'message': '登录成功!', 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwibG9naW50aW1lIjoiMjAyMS0wNS0yMCAxNjo1NDoxNC43MTcxOTMifQ.hpQIpolvCtGbnLXBd8OkUAfeICWUsSGZ-46sCLg2Vk4'}
print(json.dumps(result))


# encoded_jwt = jwt.encode({'username':'admin','password':'123456'},'secret_key',algorithm='HS256')

# print(encoded_jwt)
print(jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwibG9naW50aW1lIjoiMjAyMS0wNS0yMCAxNjo1NDoxNC43MTcxOTMifQ.hpQIpolvCtGbnLXBd8OkUAfeICWUsSGZ-46sCLg2Vk4','secret_key',algorithms=['HS256']))
# print(jwt.decode(encoded_jwt[:-1]+'b','secret_key',algorithms=['HS256']))
