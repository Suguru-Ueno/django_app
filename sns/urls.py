from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:page>', views.index, name='index'),
  path('groups', views.groups, name='groups'),
  path('add', views.add, name='add'),
  path('creategroup', views.creategroup, name='creategroup'),
  path('share/<int:share_id>', views.share, name='share'),
  path('good/<int:good_id>', views.good, name='good'),
]