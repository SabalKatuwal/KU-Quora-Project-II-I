from django.shortcuts import render
from ku_quora.models import Post,PostImages
from .models import SavedPosts
from django.http import JsonResponse
from notification.models import Notification
import json

# Create your views here.
def saved_view(request):
   
    saved_post_ids = []
    saved_objs = SavedPosts.objects.filter(user = request.user).all()
    for obj in saved_objs:
        saved_post_ids.append(obj.post.id)
    
    print(saved_post_ids , saved_objs)
    # notification_count = Notification.objects.filter(user=request.user,is_seen=False).count()
    images = PostImages.objects.all()

    context = {
        # 'notification_count':notification_count,
        'saved_posts':saved_objs,
        'saved_post_ids':saved_post_ids,
        'images':images,
    }
    return render(request,'saved/saved_page.html',context)

def save_post_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data['post_id']
        post = Post.objects.get(id = post_id)
        user = request.user
        status = '';
        if SavedPosts.objects.filter(user = user , post = post).count():
            SavedPosts.objects.filter(user = user , post = post).delete()
            status = 'unsaved'
        else:
            SavedPosts.objects.create(user = user , post = post)    
            status = 'saved'
        response = {
            'status':status
        }            

        return JsonResponse(response)