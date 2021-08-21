"""fEN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


from rest_framework import routers

router = routers.DefaultRouter()

from accounts import api

urlpatterns = [
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('app/', admin.site.urls),
    path('users/', include('users.urls')),
    path('others/', include(router.urls)),
    path('data', api.generalModelViewSet.as_view()),
] 

router.register(r'images', api.ImageViewSet)

urlpatterns += router.urls

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # from django.conf.urls import url
    # # Serve static and media files from development server
    # from django.views.static import serve
    # urlpatterns = [
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': 
    #     settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': 
    #     settings.STATIC_ROOT}),
    # ] + urlpatterns
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    

app_name = "root"
admin.site.site_header = "Family Enterprises"
admin.site.site_title = "Family Enterprises Accounting"
admin.site.index_title = "Welcome to Family Enterprises"
