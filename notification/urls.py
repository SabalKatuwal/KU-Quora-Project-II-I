from django.urls import path
from . import views

urlpatterns = [
    path('',views.notification_view,name='notification'),
    path('getLatestNotification',views.getLatestNotification_view,name='latest_notification'),
    path('notification_seen_status',views.notification_seen_status_view,name='notification_seen_status')
]