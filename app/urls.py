from django.urls import path

from app.views import *

urlpatterns = [
    #path("", views.index, name='index'),
    path("", LoginView.as_view(), name='login')
]
