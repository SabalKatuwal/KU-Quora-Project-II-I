from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = ((1,'upVote'),(2,'follow'),(3,'post'),(4,'answer'),(5,'comment'))

    post = models.ForeignKey('ku_quora.Post', on_delete=models.CASCADE,blank=True,null=True)
    answer = models.ForeignKey('ku_quora.Answer', on_delete=models.CASCADE,blank=True,null=True)
    # comment = models.ForeignKey('ku_quora.Comment', on_delete=models.CASCADE,blank=True,null=True)
    
    user_from = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notification_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE,blank = True,null=True,related_name='notification_to')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES,default=0,blank=False,null=False)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    
