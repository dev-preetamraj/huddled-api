from django.urls import path
from accounts import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('upload-user-picture/<str:slug>', views.update_user_picture, name='update_user_picture')
]
