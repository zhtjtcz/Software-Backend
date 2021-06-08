from django.db import models

# Create your models here.

class Inform(models.Model):
	ID = models.IntegerField(primary_key = True)
	type = models.IntegerField()
	userid = models.IntegerField()
	text = models.CharField(max_length = 100)
	isread = models.BooleanField()
	score = models.BooleanField()

class Score(models.Model):
	applyid = models.IntegerField()
	informid = models.IntegerField()