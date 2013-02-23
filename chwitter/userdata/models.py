from django.db import models

# Create your models here.

class Chweets(models.Model):
	user = models.CharField(max_length = 100)
	chweet = models.CharField(max_length = 141)
	timestamp = models.DateTimeField(auto_now_add = True)

class Following(models.Model):
	user = models.CharField(max_length = 100)
	following = models.CharField(max_length = 100)
