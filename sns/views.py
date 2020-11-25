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
def group(request):
  #自分が登録したfriendsを取得
  friends = Friend.objects.filter(owner=request.user)

  #POST時の処理
  if request.method == 'POST':

    #Groupsメニューの選択肢の処理
    if request.POST['mode'] == '__groups_form__': #ここは調べる
      #選択したGroup名を取得
      sel_group = request.POST['groups']
      #Groupを取得
      gp = Group.objects.filter(owner=request.user).filter(title=sel_group).first()
      
      #Groupに含まれるFriendを取得
      fds = Friend.objects.filter(owner=request.user).filter(group=gp)
      print(Friend.objects.filter(owner=request.user))

      #FriendのUserをリストにまとめる
      vlist =[]
      for item in fds:
        vlist.append(item.user.username)

      #フォームの用意
      groupsform = GroupSelectForm(request.user, request.POST)
      friendsform = FriendsForm(request.user, friends=friends, vals=vlist)

    #Friendsのチェック更新時の処理
    if request.POST['mode'] == '__friends_form__':
      #選択したGroupの取得
      sel_group = request.POST['group']
      group_obj = Group.objects.filter(title=sel_group).first()
      print(group_obj)
      #チェックしたFriendsの取得
      sel_fds = request.POST.getlist('friends')
      #FriendsのUserの取得
      sel_user = User.objects.filter(username__in=sel_fds)
      #Userのリストに含まれるユーザーが登録したFriendを取得
      fds = Friend.objects.filter(owner=request.user).filter(user__in=sel_user)
      #すべてのFriendにGroupを設定する
      vlist = []
      for item in fds:
        item.group = group_obj
        item.save()
        vlist.append(item.user.username)
      #メッセージを設定
      messages.success(request, 'チェックされたFriendを'+sel_group+'に登録しました')
      #フォームの用意
      groupsform = GroupSelectForm(request.user, {'groups':sel_group})
      friendsform = FriendsForm(request.user, friends=friends, vals=vlist)
  #GET時の処理
  else:
    #フォームの用意
    groupsform = GroupSelectForm(request.user)
    friendsform = FriendsForm(request.user, friends=frieds, vals=[])
    sel_group = '-'
  
  #共通の処理
  createform = CreateGroupForm()
  params = {
    'login_user':request.user,
    'groups_form':groupsform,
    'create_form':createform,
    'friend_form':friendsform,
    'group':sel_group,
  }
  return render(request, 'sns/group.html', params)

#Friendの追加処理
@login_required(login_url='/admin/login/')
def add(request):
  #追加するUserを取得
  add_name = request.GET['name']
  add_user = User.objects.filter(username=add_name).first()
  #Userが本人だった場合
  if add_user == request.user:
    messages.info(request, "自分自身をFriendに追加することはできません。")
    return redirect(to='/sns')
  #publicの取得
  (public_user, public_group) = get_public()
  #add_userのFrendの数を調べる
  frd_num = Friend.objects.filter(owner=request.user).filter(user=add_user).count()
  #frd_num > 0 ならば、すでに登録済み
  if frd_num > 0:
    messages.info(request, add_user.username+'はすでに登録されています。')
    return redirect(to='/sns')
  
  #Friendの登録処理
  frd = Friend()
  frd.owner = request.user
  frd.group = public_group
  frd.save()

  #messageを設定
  messages.success(request, add_user.username+'を追加しました。groupページに移動して、追加したFriendをメンバーに設定してください。')
  return redirect(to='/sns')
  
