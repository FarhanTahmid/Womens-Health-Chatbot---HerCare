from django.db import models

# Create your models here.

class ApplicationUser(models.Model):
    username=models.CharField(max_length=100,null=False,blank=False)
    choice_of_convo_remembering=models.BooleanField(null=False,blank=False,default=False)
    
    
    class Meta:
        verbose_name = "Application Users"
    
    def __str__(self) -> str:
        return self.username