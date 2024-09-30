from django.db import models
from user.models import ApplicationUser
# Create your models here.

class UserConversationThreads(models.Model):
    username=models.ForeignKey(ApplicationUser,on_delete= models.CASCADE)
    thread_id=models.CharField(max_length=200,null=False,blank=False)

    
    class Meta:
        verbose_name = "User Conversation Threads"
    
    def __str__(self) -> str:
        return str(self.pk)