from django.db import models

# Create your models here.

class Main(models.Model):
	ID = models.IntegerField(primary_key = True)
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	email = models.CharField(max_length = 30)
	wxid = models.CharField(max_length = 20)