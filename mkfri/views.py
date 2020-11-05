from django.shortcuts import render
from django.http import HttpResponse
from .forms import HelloForm

# Create your views here.

def index(request):
  params = {
    'title': 'mkfri/index',
    'msg' : '名前を入力してください。',
    'goto' : 'next',
    'form' : HelloForm(),
  }

  if (request.method == 'POST'):
    params['msg'] = '名前:' + request.POST['name'] + '<br>メール:' + request.POST['mail'] + '<br>年齢:' + request.POST['age']
    params['form'] = HelloForm(request.POST)

  return render(request, 'mkfri/index.html', params)


