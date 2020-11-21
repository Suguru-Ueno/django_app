from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#Messageクラスの定義
class Message(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_owner')
  group = models.ForeignKey('Group',on_delete=models.CASCADE)
  content = models.TextField(max_length=1000)
  share_id = models.IntegerField(default=-1)
  good_count = models.IntegerField(default=0)
  share_count = models.IntegerField(default=0)
  put_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.content) + '(' + str(self.owner) + ')'

  def get_share(self):
    return Message.objects.get(id=self.share_id)
  
  class Meta:
    ordering = ('-put_date',)



#Groupクラスの定義
class Group(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_owner')
  title = models.CharField(max_length=100)

  def __str__(self):
    return '<' + self.title + '(' + str(self.owner) + ')>'


#Friendクラスの定義
class Friend(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_owner')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.user) + '(group:"' + str(self.group) + '")'

#Goodクラスの定義
class Good(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_owner')
  message = models.ForeignKey(Message, on_delete=models.CASCADE)

  def __str__(self):
    return 'good for"' + str(self.message) + '"by' + str(self.owner) + ')'

