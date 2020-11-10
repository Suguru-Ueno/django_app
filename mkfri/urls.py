from django.conf.urls import url
# from .views import HelloView
from django.urls import path
from . import views
urlpatterns = [
  path('', views.index, name = "index"),
  path('create', views.create, name ="create")
]