from django.contrib import admin
from user.models import *

class UserMain(admin.ModelAdmin):
	list_display = ['ID', 'username', 'password', 'email', 'wxid']
admin.site.register(Main, UserMain)