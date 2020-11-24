from django import forms
from .models import Friend, Group, Good, Message
from django.contrib.auth.models import User

#Messageフォーム
class MessageForm(forms.ModelForm):
  class Meta:
    model = Message
    fields = ['owner', 'group', 'content']

#Groupフォーム
class GroupForm(forms.ModelForm):
  class Meta:
    model = Group
    fields = ['owner', 'title']

#Friendフォーム
class FriendForm(forms.ModelForm):
  class Meta:
    models = Friend
    fields = ['owner', 'user', 'group']

#Goodフォーム
class GoodForm(forms.ModelForm):
  class Meta:
    model = Good
    fields = ['owner', 'message']

#Groupのチェックボックスフォーム
class GroupCheckForm(forms.Form):
  def __init__(self, user, *args, **kwargs):
    super(GroupCheckForm, self).__init__(*args, **kwargs)
    public = User.objects.filter(username='public').first()
    self.fields['groups'] = forms.MultipleChoiceField(choices=[(item.title, item.title) for item in Group.objects.filter(owner__in=[user, public])], widget=forms.CheckboxSelectMultiple(),)

