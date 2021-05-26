from django.db import models

# Create your models here.

class Category(models.Model):
	catid = models.IntegerField(primary_key = True)
	category = models.CharField(max_length = 20)
	count = models.IntegerField()

class GImg(models.Model):
	imgid = models.IntegerField(primary_key = True)
	goodid = models.IntegerField(blank = True)
	img = models.ImageField(blank = True)

class GoodInfo(models.Model):
	goodid = models.IntegerField(primary_key = True)
	userid = models.IntegerField()
	goodname = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200)
	categoryid = models.IntegerField()
	uploadtime = models.CharField(max_length = 50)
	price = models.FloatField()
	onsale = models.BooleanField()

class GoodCollect(models.Model):
	userID = models.IntegerField()
	goodID = models.IntegerField()