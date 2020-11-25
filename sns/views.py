from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Message, Friend, Group, Good
from .forms import GroupCheckForm, GroupSelectForm, FriendsForm, CreateGroupForm, PostForm

#indexのview関数
@login_required(login_url='/admin/login/')
def index(request, page=1):
  #publicのuserを取得
  (public_user, public_group) = get_public()

  #POST時の処理
  if request.method == 'POST':
    #Groupsのチェックを更新したときの処理
    #フォームの用意
    checkform = GroupCheckForm(request.user, request.POST)
    #request.userは、ログイン中のユーザーデータを取得している

    #チェックされたGroup名をリストにまとめる
    glist = []
    for item in request.POST.getlist('groups'):
    #.getlist name属性が同じinputタグが複数あるとき、そのname属性をもつ値をリストですべて取得する
    #request.POST['groups']で取得すると複数ある場合、最後の一つしか取得できない
      glist.append(item)
    
    #Messageの取得
    messages = get_your_group_message(request.user, glist, page)
  
  #GET時の処理
  else:
    #フォームの用意
    checkform = GroupCheckForm(request.user)
    #Groupのリストを取得
    gps = Group.objects.filter(owner=request.user)
    glist = [public_group.title]
    for item in gps:
      glist.append(item)
    #メッセージの取得
    messages = get_your_group_message(request.user, glist, page)
  
  #共通の処理
  params = {
    'login_user':request.user,
    'contents':messages,
    'check_form':checkform,
  }
  return render(request, 'sns/index.html', params)



@login_required(login_url='/admin/login/')
def 