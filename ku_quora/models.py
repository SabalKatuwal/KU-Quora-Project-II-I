from notification.views import notification_seen_status_view
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
User = get_user_model()
from django.utils.text import slugify
from django.urls import reverse
from notification.models  import  Notification
from django.db.models.signals import post_save,post_delete,pre_delete,m2m_changed
import os
from core.settings import BASE_DIR

from account.models import Follow

from django.contrib.auth.models import User
from django.utils.timezone import now



def get_file_path(instance,filename):
    subfolder = 'postimages'
    return os.path.join(str(instance.post.user.id),subfolder,filename)

class Tag(models.Model):
    title = models.CharField(max_length = 30)
    slug = models.SlugField(null=True,unique=True,blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tags',args=[self.slug])
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        print('slug : ',self.slug)
        return super().save(*args,**kwargs)
   
   
class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    title = models.CharField(max_length=100)
    body = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=False,unique=True,blank=True)

    def get_total_answer_count(self):
        return Answer.objects.filter(post=self).count()

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.id])
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title + str(self.posted_on))
        return super().save(*args,**kwargs)
    
    def notify_post(sender,instance,*args,**kwargs):
        user_from = instance.user
        post = instance
        # user_to = followers objs
        notification_type = 3
        
        objs = Follow.objects.filter(following=user_from).all()
        for obj in objs:
            notification = Notification(user_from=user_from,user_to=obj.follower,notification_type=notification_type,post=post)
            notification.save()


class Answer(models.Model):
    ansID = models.AutoField( primary_key= True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #parent = models.ForeignKey('self', on_delete=models.CASCADE, null= True)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    upVotes = models.ManyToManyField(User,related_name='likes')

    def get_total_upVotes(self):
        return self.upVotes.count()

    def __str__(self):
        return '%s - %s' %(self.post.title, self.user)

    def notify_answer(sender,instance,*args,**kwargs):
        user_from = instance.user
        user_to = instance.post.user
        notification_type = 4
        post = instance.post
        answer = instance

        Notification.objects.create(answer=answer,user_from=user_from,user_to=user_to,notification_type=notification_type,post=post)
        print('answer notified')
        # notification.save()
    
    def notify_upVote(sender,instance,action,reverse,pk_set,**kwargs):
        if action == "post_add":
            print('instance:',instance.body)
            print('sender:',sender)
            print('post_add:',pk_set)
            pk = list(pk_set).pop()
            print(pk)
            user_from = User.objects.get(id=pk)
            user_to = instance.user
            notification_type = 1
            answer = instance
            if user_from != user_to:
                Notification.objects.create(notification_type=notification_type,user_from=user_from,user_to=user_to,answer=answer)

    # def notify_upVote(sender,instance,action,)

class AnswerImages(models.Model):
    answer = models.ForeignKey(Answer, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'answerImages/')

    def deleteImage(sender,instance,*args,**kwargs):
        instance.image.delete()
        print('image deleted')

class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = get_file_path)
    
    def deleteImage(sender,instance,*args,**kwargs):
        instance.image.delete()
        print('image deleted')
      
class Comment(models.Model):
    commentId= models.AutoField(primary_key= True)
    answer = models.ForeignKey(Answer, on_delete= CASCADE)
    user = models.ForeignKey(User, on_delete= CASCADE)
    # parent = models.ForeignKey('self', on_delete=CASCADE)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' %(self.body, self.user)

    def notify_comment(sender,instance,*args,**kwargs):
        user_from = instance.user
        user_to = instance.answer.user
        notification_type = 5
        post = instance.answer.post
        answer = instance.answer
        if user_from != user_to:
            Notification.objects.create(answer=answer,user_from=user_from,user_to=user_to,notification_type=notification_type,post=post)
            print('comment notified')


pre_delete.connect(PostImages.deleteImage,sender=PostImages)
pre_delete.connect(AnswerImages.deleteImage,sender=AnswerImages)
post_save.connect(Post.notify_post,sender=Post)
post_save.connect(Answer.notify_answer,sender=Answer)
post_save.connect(Comment.notify_comment , sender = Comment)
m2m_changed.connect(Answer.notify_upVote,sender=Answer.upVotes.through)

