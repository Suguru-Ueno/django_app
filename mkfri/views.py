from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import FriendForm,HelloForm
from .models import Friend 

# Create your views here.

# class HelloView(TemplateView):

#   def __init__(self):
#     self.params = {
#       'title' : 'mkfri/index',
#       'msg' : 'あなたの情報を入力してください。',
#       'form' : HelloForm(),
#     }

#   def get(self, request):
#     return render(request, 'mkfri/index.html', self.params)

#   def post(self, request):
#     self.params['msg'] = '名前:' + request.POST['name'] + '<br>メール:' + request.POST['mail'] + '<br>年齢:' + request.POST['age']
#     self.params['form'] = HelloForm(request.POST)
#     return render(request, 'mkfri/index.html', self.params)
  


def index(request):
  data = Friend.objects.all()
  params = {
    'title' : 'hello my friends',
    'msg' : 'they are my friends',
    'form' : HelloForm(),
    'data' : data,
  }
  return render(request, 'mkfri/index.html', params)
   

def create(request):
  if (request.method == 'POST'):
    obj = Friend()
    friend = FriendForm(request.POST, instance = obj)
    friend.save()
    return redirect(to='/mkfri')
  params = {
    'title':'Hello',
    'form':FriendForm(),
  }
  return render(request, 'mkfri/create.html', params)