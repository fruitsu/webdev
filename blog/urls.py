from django.urls import path, include
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.login, name='login'),
    path('edit/', views.edit_com, name='edit_com'),
    path('list', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('social/', include('social_django.urls', namespace="social")),
    path('accounts/', include('django.contrib.auth.urls'), {'next_page': '/blog/forms/'}),
    path('post/add_comm', views.add_comm, name='add_comm'),
    path('post/detail', views.post_detail, name='post_detail'),

]
