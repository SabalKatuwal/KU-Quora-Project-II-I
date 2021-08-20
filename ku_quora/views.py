from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Tag,PostImages,Answer,AnswerImages,Comment
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from notification.models import Notification
from saved.models import SavedPosts
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.core import serializers
import string
from django.utils.text import slugify
from django.contrib import messages
from better_profanity import profanity

@login_required(login_url='login')
def index_view(request):
    # posts = Post.objects.all().order_by('-posted_on')
    posts = Post.objects.all().order_by('?')
    saved_post_ids = []
    saved_objs = SavedPosts.objects.filter(user = request.user).all()
    for obj in saved_objs:
        saved_post_ids.append(obj.post.id)
    images = PostImages.objects.all()
    context = {
        'posts':posts,
        'images':images,
        'saved_post_ids':saved_post_ids,
    }
    return render(request,'ku_quora/index.html',context)


def create_post_view(request):
    if request.method == 'POST':
        user = request.user
        tags_objs = []
        title = request.POST.get('title')
        # title = profanity.censor(title,'*')
        body = request.POST.get('body')
        # body = profanity.censor(body,'*')
        tags = request.POST.get('tags')
        images = request.FILES.getlist('image1')
        p, created = Post.objects.get_or_create(title=title,body=body,user=user)
        tags_list = list(tags.split('#'))
        print('list = ',list)
        for tag in tags_list:
            # tag = profanity.censor(tag,'*')
            t , created = Tag.objects.get_or_create(title=tag)
            print('t = ' , t)
            tags_objs.append(t)
        p.tags.set(tags_objs)
        for image in images:
            i, created = PostImages.objects.get_or_create(post=p,image=image)
        return redirect('index')

def post_detail_view(request,post_id):
    post = get_object_or_404(Post,id = post_id)
    saved_post_ids = []
    saved_objs = SavedPosts.objects.filter(user = request.user).all()
    for obj in saved_objs:
        saved_post_ids.append(obj.post.id)
    p = Post.objects.get(id=post_id)
    images = PostImages.objects.filter(post=p)
    
    answers = Answer.objects.filter(post=post).order_by('-time')
    answerImages = []
    UpVotedAnswerIds = []


    for answer in answers:
        if answer.upVotes.filter(id=request.user.id):
            UpVotedAnswerIds.append(answer.ansID)
        images = AnswerImages.objects.filter(answer=answer).all()
        for image in images:
            answerImages.append(image)
    comments = Comment.objects.all()
    print(comments)

   

    detail = 1
    context = {
        'post':post,
        # 'notification_count':notification_count,
        'images':images,
        'answerImages':answerImages,
        'saved_post_ids':saved_post_ids,
        'answers':answers,
        'UpVotedAnswerIds':UpVotedAnswerIds,
        'inDetailView':detail,
        'comments':comments
    }
    return render(request,'ku_quora/post_detail.html',context)


def tags_post_view(request,tag_slug):
    saved_post_ids = []
    saved_objs = SavedPosts.objects.filter(user = request.user).all()
    for obj in saved_objs:
        saved_post_ids.append(obj.post.id)
    
    tag = get_object_or_404(Tag,slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted_on')
    # notification_count = Notification.objects.filter(user=request.user,is_seen=False).count()
    images = PostImages.objects.all()
    context = {
        'posts':posts,
        'tag':tag,
        # 'notification_count':notification_count,
        'saved_post_ids':saved_post_ids,
        'images':images
    }
    return render(request,'ku_quora/tag_post.html',context)


def delete_post_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data['post_id']
        Post.objects.filter(id = post_id).delete()
        
        response = {
            'deleted':True
        }            

        return JsonResponse(response)
    return redirect('index')

# def AnswerView(request):
#     if request.method == "POST":
#         answer=request.POST.get('answer')
#         user=request.user
#         postSno =request.POST.get('postSno')
#         post= Post.objects.get(id=postSno)
#         answer=Answer(answer= answer, user=user, post=post)
#         answer.save()
#         return redirect(f"/{post.id}")        
        
def addAnswerNew_view(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        body = request.POST.get('answer')  
        post = Post.objects.get(id=post_id)
        answer = Answer.objects.create(post=post,user=request.user,body=body)
        OutImages = []
        for file in request.FILES:
            image = request.FILES.get(file)
            i = AnswerImages.objects.create(answer=answer,image=image)
            i.save()

        Images = AnswerImages.objects.filter(answer=answer)
        for image in Images:
            OutImages.append(str(image.image))
            
        response = {
            'author':request.user.username,
            'body':body,
            'time':answer.time,
            'profile_pic':answer.user.profile.profile_pic.url,
            'images':OutImages
        }

        return JsonResponse(response)
        

def deleteAnswer_view(request):
    if request.method == 'POST':
        answerId = request.POST.get('button')
        answer = Answer.objects.get(ansID=answerId)
        post = answer.post
        answer.delete()
        return redirect('post_detail',post.id)

def post_upVote_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        answerId = data['answerId']
        answer =get_object_or_404( Answer,ansID = answerId)
        UpVoted = False
        if answer.upVotes.filter(id = request.user.id ).exists():
            answer.upVotes.remove(request.user)
            UpVoted = False
        else:
            answer.upVotes.add(request.user)
            UpVoted = True

        response = {
            'upVoteCount' : answer.get_total_upVotes(),
            'upVoted':UpVoted
        }

        return JsonResponse(response)


def post_comment_view(request):
    if request.method == "POST":
        comment_body = request.POST.get('comment_body')
        user=request.user
        answerId =request.POST.get('answerId')
        answer= Answer.objects.get(ansID=answerId)
        Comment.objects.create(body = comment_body, user=user, answer=answer)
        return redirect('post_detail',answer.post.id) 
    return render(request,'ku_quora/index.html',{})



def post_edit_view(request,post_id):
    

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags = request.POST.get('tags')
        images = request.FILES.getlist('images')
        print(images)
        Post.objects.filter(id=post_id).update(title=title,body=body)
        tags_objs = []
        p = Post.objects.get(id=post_id)      
        tags_list = list(tags.split('#'))
        for tag in tags_list:
            t , created = Tag.objects.get_or_create(title=tag)
            tags_objs.append(t)
        p.tags.set(tags_objs)
        p.save()
        for image in images:
            i, created = PostImages.objects.get_or_create(post=p,image=image)
        messages.success(request,f"Post Edited successfully")
        return redirect('/')

    post = Post.objects.get(id = post_id)
    tags = post.tags.all()
    images = PostImages.objects.filter(post=post)
    context = {
        'post':post,
        'tags' : tags,
        'images':images
    }

    return render(request,'ku_quora/edit_post.html',context)


def search(request):
    sq = request.GET.get('sq')
    post_ids = []
    if(sq == ''):
        count = 0
    else:
        PostFromTitle = Post.objects.filter(title__icontains=sq);
        for post in PostFromTitle:
            post_ids.append(post.id)
        tags = Tag.objects.filter(title__icontains=sq);
        for tag in tags:
            posts = tag.post_set.all()
            for post in posts:
                if post.id not in post_ids:
                    post_ids.append(post.id)
        
        PostFromBody = Post.objects.filter(body__icontains=sq)
        for post in PostFromBody:
            if post.id not in post_ids:
                post_ids.append(post.id)
        count = len(post_ids)
    allPosts = []
    for id in post_ids:
        p = Post.objects.get(id=id)
        allPosts.append(p)
    print(allPosts)
    context = {
        'allPosts':allPosts,
        'query':sq,
        'count':count
    }
    return render(request,'ku_quora/search.html',context)


def delete_post_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        imageId = data['imageId']
        print(imageId)
        PostImages.objects.filter(id=imageId).delete()
        response = {
            'deleted':True
        }

        return JsonResponse(response)