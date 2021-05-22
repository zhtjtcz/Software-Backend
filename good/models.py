from django.db import models

# Create your models here.

class Category(models.Model):
	catid = models.IntegerField(primary_key = True)
	category = models.CharField(max_length = 20)
	count = models.IntegerField()

class GoodImg(models.Model):
	imgid = models.IntegerField(primary_key = True)
	img = models.ImageField(blank = True)