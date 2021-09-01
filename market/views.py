from django.shortcuts import render
import jazzmin

def NotificationView(request, user_id=None):
    return render(request, template_name="market/notifications.html", context={'request':request})
