from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-gallery/', views.my_gallery, name='my_gallery'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('signup/', views.signup, name='signup'),
    path('upload/', views.photo_upload, name='photo_upload'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:pk>/edit/', views.photo_edit, name='photo_edit'),
    path('photo/<int:pk>/delete/', views.photo_delete, name='photo_delete'),
    path('photo/<int:pk>/like/', views.like_photo, name='like_photo'),
    path('photo/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]
