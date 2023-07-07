from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import serve
from django.urls import path, include
from board.views import AdList, AdDetail, AdCreate, AdUpdate, AdDelete, Comments, delete, accept
from billboard import settings
# from rest_framework import routers


urlpatterns = [
    path('', AdList.as_view(), name='ad_list'),
    path('create/', AdCreate.as_view(), name='create_ad'),
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('<int:pk>/update/', AdUpdate.as_view(), name='ad_edit'),
    path('<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
    path('<int:pk>/add_comment/', AdDetail.as_view(), name='add_comment'),
    path('comments/', Comments.as_view(), name='comments'),
    path('<int:pk>/accept/', accept, name='accept_comment'),
    path('<int:pk>/decline/', delete, name='delete_comment'),
]


# add condition in django urls file
if settings.DEBUG:
    urlpatterns += [path(settings.MEDIA_URL[1:], serve, {"document_root": settings.MEDIA_ROOT})]
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
