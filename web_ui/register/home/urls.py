from django.urls import path

from home import views

app_name = 'homes'

urlpatterns = [
    path('', views.index, name="index"),
]
