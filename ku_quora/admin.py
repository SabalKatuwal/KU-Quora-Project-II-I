from django.contrib import admin
from .models import Tag,Post,PostImages,Answer,AnswerImages,Comment
from django.contrib.sessions.models import Session
# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(PostImages)
admin.site.register(Session)
admin.site.register(Answer)
admin.site.register(AnswerImages)
admin.site.register(Comment)


