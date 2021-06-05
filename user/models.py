from django.db import models

# Create your models here.

class Main(models.Model):
	ID = models.IntegerField(primary_key = True)
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	email = models.CharField(max_length = 30)
	wxid = models.CharField(max_length = 20, blank = True)

class EmailCode(models.Model):
	code = models.CharField(max_length = 50)

class Userheadshot(models.Model):
	userID = models.IntegerField(primary_key = True)
	headshot= models.ImageField(blank = True)

class UserInfo(models.Model):
	userID = models.IntegerField(primary_key = True)
	sex = models.IntegerField(blank = True, null = True)
	grade = models.IntegerField(blank = True, null = True)
	telephone = models.CharField(max_length=15, blank = True)
	location = models.IntegerField(blank = True, null = True)
	tradecount = models.IntegerField(blank = True, null = True)
	score = models.FloatField(blank = True, null = True)

class UserFollow(models.Model):
	userID = models.IntegerField()
	followID = models.IntegerField()

class BanInfo(models.Model):
	userID = models.IntegerField(primary_key = True)