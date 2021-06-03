from django.db import models

# Create your models here.

class Trade(models.Model):
	ID = models.IntegerField(primary_key = True)
	objectID = models.IntegerField()
	type = models.IntegerField()
	ownID = models.IntegerField()
	requestID = models.IntegerField()
	status = models.IntegerField()
	score = models.FloatField()