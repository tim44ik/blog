from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('post/<str:pk>',views.post, name='post'),
    path('create_post', views.create_post, name='create_post'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('delete/<str:pk>', views.remove, name='delete_post'),
    path('edit/<str:pk>', views.edit, name='edit_post')
]
