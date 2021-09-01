from django.urls import path, include
import market.views as marketViews

urlpatterns = [
  path('', marketViews.NotificationView, name="notifier"),
  
]

app_name='market'