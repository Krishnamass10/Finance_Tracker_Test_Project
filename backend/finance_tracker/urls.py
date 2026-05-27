from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('apps.users.urls')),

    path(
        'transactions/',
        include('apps.transactions.urls')
    ),

    path(
        'dashboard/',
        include('apps.dashboard.urls')
    ),

    path(
        'reports/',
        include('apps.exports.urls')
    ),

    path(
        'chatbot/',
        include('apps.chatbot.urls')
    ),
]