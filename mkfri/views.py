from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from .forms import FriendForm,HelloForm,FindForm,MessageForm
from .models import Friend , Message

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
  


def index(request, num = 1):
  if (request.method == 'POST'):
    form = FindForm(request.POST)
    find = request.POST['find']
    data = Friend.objects.filter(name__icontains=find)
    page = Paginator(data, 5)
    msg = '検索結果数は' + str(data.count())
  else:
    msg = '友達の名前で検索するよ。'
    form = FindForm()
    data = Friend.objects.all()
    page = Paginator(data, 5)
  params = {
    'title' : 'hello my friends',
    'msg' : msg,
    'data' : page.get_page(num),
    'form' : form, 
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


def edit(request, num):
  obj = Friend.objects.get(id = num)
  if (request.method == 'POST'):
    friend = FriendForm(request.POST, instance=obj)
    friend.save()
    return redirect(to='/mkfri')
  params ={
    'title' : '友達の編集',
    'id' : num,
    'form' : FriendForm(instance=obj),
  }
  return render(request, 'mkfri/edit.html', params)

def delete(request,num):
  friend = Friend.objects.get(id=num)
  if (request.method == 'POST'):
    friend.delete()
    return redirect(to='/mkfri')
  params ={
    'title' : '友達のデータを消去する',
    'msg' : '本当に良いですか？',
    'id' : num,
    'obj' : friend
  } 
  return render(request, 'mkfri/delete.html', params)

def message(request, page=1):
  if (request.method == 'POST'):
    obj = Message()
    form = MessageForm(request.POST,instance=obj)
    form.save()
  data = Message.objects.all().reverse()
  paginator = Paginator(data,5)
  params = {
    'title': 'Message一覧',
    'form': MessageForm(),
    'data': paginator.get_page(page),
  }
  return render(request, 'mkfri/message.html', params)