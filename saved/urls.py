from django.urls import path
from . import views

urlpatterns = [
    path('',views.saved_view,name = 'saved'),
    path('save_post/',views.save_post_view,name = 'save_post'),
]