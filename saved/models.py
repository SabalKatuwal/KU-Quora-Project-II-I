from django.db import models
from django.contrib.auth import get_user_model
from ku_quora.models import Post

User = get_user_model()

# Create your models here.
class SavedPosts(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)