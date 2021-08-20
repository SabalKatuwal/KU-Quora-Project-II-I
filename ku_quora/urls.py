from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view,name='index'),
    path('create_post/',views.create_post_view,name='create_post'),
    path('delete/',views.delete_post_view,name = 'delete_post'),
    path('addAnswer/',views.addAnswerNew_view),
    path('post/upVote',views.post_upVote_view,name="post_upVote"),
    path('deleteAnswer/',views.deleteAnswer_view,name = "deleteAnswer"),
    path('post/<uuid:post_id>/',views.post_detail_view,name='post_detail'),
    path('postComment/',views.post_comment_view),
    path('search/',views.search , name="search"),
    path('PostEdit/<uuid:post_id>',views.post_edit_view,name="post_edit"),
    path('deletePostImage/',views.delete_post_image),
    path('tag/<slug:tag_slug>',views.tags_post_view,name='tags'),
]