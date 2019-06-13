from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(template_name='registration/login.html', next_page='/'), name='logout'),
    path('', include('blog.urls')),
    path('register/', user_views.register, name="register"),
]
