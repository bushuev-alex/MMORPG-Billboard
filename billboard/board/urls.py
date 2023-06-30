from django.contrib import admin
from django.urls import path, include
from board.views import AdList, AdDetail, AdCreate, Comments, delete, accept

# from rest_framework import routers


urlpatterns = [
    path('', AdList.as_view(), name='ad_list'),
    path('create/', AdCreate.as_view(), name='create_ad'),
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('<int:pk>/add_comment/', AdDetail.as_view(), name='add_comment'),
    path('comments/', Comments.as_view(), name='comments'),
    path('<int:pk>/accept/', accept, name='accept_comment'),
    path('<int:pk>/decline/', delete, name='delete_comment'),
]
