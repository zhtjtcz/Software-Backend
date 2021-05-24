from django.db import models

# Create your models here.

class DemandInfo(models.Model):
	demandid = models.IntegerField(primary_key = True)
	userid = models.IntegerField()
	demandname = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200)
	categoryid = models.IntegerField()
	uploadtime = models.CharField(max_length = 50)
	price = models.FloatField()
	onsale = models.BooleanField()