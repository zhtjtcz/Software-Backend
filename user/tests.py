from django.test import TestCase
import requests
import pandas
import openpyxl
import jwt

# res = requests.post('http://123.57.194.168:8000/login/', data={'username':'AAA', 'password':'111'})
# res = requests.post('http://127.0.0.1:8000/email/', data={'email':'18377221@buaa.edu.cn', 'password':'123456'})
# print(res.text)

encoded_jwt = jwt.encode({'username':'admin','password':'123456'},'secret_key',algorithm='HS256')

print(encoded_jwt)
print(jwt.decode(encoded_jwt,'secret_key',algorithms=['HS256']))
print(jwt.decode(encoded_jwt[:-1]+'b','secret_key',algorithms=['HS256']))