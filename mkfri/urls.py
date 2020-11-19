from django.conf.urls import url
# from .views import HelloView
from django.urls import path
from . import views
urlpatterns = [
  path('', views.index, name = "index"),
  path('<int:num>', views.index, name = "index"),
  path('create', views.create, name ="create"),
  path('create/<int:num>', views.edit, name='edit'),
  path('delete/<int:num>', views.delete, name='delete'),
  path('message/', views.message, name='message'),
  path('message/<int:page>', views.message, name='message'),

]