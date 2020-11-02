from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
  params = {
    'title': 'Hello/indexの1',
    'msg' : 'This is a pample page',
    'goto' : 'next',
  }
  return render(request, 'mkfri/index.html', params)

def next(request):
  params = {
    'title': 'Hello/indexの2',
    'msg' : 'This is a pample page',
    'goto' : 'index',
  }
  return render(request, 'mkfri/index.html', params)