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

#グループの作成処理
@login_required(login_url='/admin/login/')
def creategroup(request):
  #Groupを作りUserとtitleを設定して、保存する
  gp = Group()
  gp.owner = request.user
  gp.title = request.user.username+'の'+request.POST['group_name']
  gp.save()
  messages.info(request, '新しいグループを作成しました。')
  return redirect(to='/sns/groups')

#メッセージのPOST処理
@login_required(login_url='/admin/login/')
def post(request):
  #POST送信の処理
  if request.method == 'POST':
    #送信内容の取得
    gr_name = request.POST['groups']
    content = request.POST['content']
    #Groupの取得
    group = Group.objects.filter(owner=request.user).filter(title=gr_name)
    if group == None:
      (pub_user, group) = get_public()
    #Messageを作成し設定して保存
    msg = Message()
    msg.owner = request.user
    msg.group = group
    msg.content = content
    msg.save()
    #メッセージを設定
    messages.success(request, '新しいメッセージを投稿しました。')
    return redirect(to='/sns')

  #GETアクセス時の処理
  else:
    form = PostForm(request.user)
  
  #共通の処理
  params = {
    'login_user':request.user,
    'form':form,
  }
  return render(request, 'sns/post.html', params)

#投稿をshare
@login_required(login_url='/admin/login/')
def share(request, share_id):
  #シェアするMessageの取得
  share = Message.objects.get(id=share_id)
  print(share)
  #POST送信時の処理
  if request.method == 'POST':
    #送信内容の取得
    gr_name = request.POST['groups']
    content = request.POST['content']
    #Groupの取得
    group = Group.objects.filter(owner=request.user).filter(title=gr_name).first()
    if group == None:
      (pub_user, group) = get_public()
    #メッセージを作成し、設定を保存
    msg = Message()
    msg.owner = request.user
    msg.group = group
    msg.content = content
    msg.share_id = share.id
    msg.save()
    share_msg = msg.get_share()
    share_msg.share_count += 1
    share_msg.save()
    #メッセージを設定
    messages.success(request, 'メッセージをシェアしました。')
    return redirect(to='/sns')
  
  #共通の処理
  form = PostForm(request.user)
  params = {
    'login_user':request.user,
    'form':form,
    'share':share,
  }
  return render(request, 'sns/share.html', params)

#goodボタンの処理
@login_required(login_url='/admin/login/')
def goood(request, good_id):
  #goodするMessageを取得
  good_msg = Message.objects.get(id=good_id)
  #自分がMessageにgoodした数を調べる
  is_good = Good.objects.filter(owner=request.user).filter(message=good_msg).count()
  #is_good > 0 ならば、既にgood済み
  if is_good > 0:
    messages.success(request, 'このメッセージは、既にgoodしました。')
    return redirect(to='/sns')
  #Messageのgood_countを1増やす
  good_msg.good_count += 1
  good_msg.save()
  #Goodを作成し、設定して保存
  good = Good()
  good.owner = request.user
  good.message = good_msg
  good.save()
  #メッセージを設定
  messages.success(request, 'メッセージにgoodしました。')
  return redirect(to='/sns')

#以下で、viewに使用する関数を定義する

#指定されたグループ及び検索文字によるMessageの取得
def get_your_group_message(owner, glist, page):
  page_num = 10 #1ページあたりの表示数
  #publicの取得
  (public_user, public_group) = get_public()
  #チェックされたGroupの取得
  
