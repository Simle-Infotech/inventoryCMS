from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, Pull, UpdatePassword
from knox import views as knox_views

urlpatterns = [
  path('auth', include('knox.urls')),
  path('auth/register', RegisterAPI.as_view()),
  path('auth/login', LoginAPI.as_view()),
  path('auth/user', UserAPI.as_view()),
  path('updatebranches', Pull.as_view()),
  path('auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
  path('auth/change', UpdatePassword.as_view()),
]

app_name='accounts'