from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import HelloForm

# Create your views here.

class HelloView(TemplateView):

  def __init__(self):
    self.params = {
      'title' : 'mkfri/index',
      'msg' : 'あなたの情報を入力してください。',
      'form' : HelloForm(),
    }

  def get(self, request):
    return render(request, 'mkfri/index.html', self.params)

  def post(self, request):
    self.params['msg'] = '名前:' + request.POST['name'] + '<br>メール:' + request.POST['mail'] + '<br>年齢:' + request.POST['age']
    self.params['form'] = HelloForm(request.POST)
    return render(request, 'mkfri/index.html', self.params)
  


