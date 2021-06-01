from django.db import models

# Create your models here.

class Msg(models.Model):
	ID = models.IntegerField(primary_key = True)
	objectID = models.IntegerField()
	type = models.IntegerField()
	sendID = models.IntegerField()
	replyID = models.IntegerField()
	text = models.CharField(max_length = 110)
	sendtime = models.CharField(max_length = 30)