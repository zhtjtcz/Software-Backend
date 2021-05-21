from django.db import models

# Create your models here.

class Category(models.Model):
	ID = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 20)
	count = models.IntegerField()