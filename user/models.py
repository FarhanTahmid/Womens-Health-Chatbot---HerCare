from django.db import models

# Create your models here.

class ApplicationUser(models.Model):
    username=models.CharField(max_length=100,null=False,blank=False)