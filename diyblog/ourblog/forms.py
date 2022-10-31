from dataclasses import field
from socket import fromshare
from django.forms import ModelForm
from .models import Comment, Post

class CommentForm(ModelForm):
   class Meta:
      model = Comment
      fields =['email', 'description']

class PostForm(ModelForm):
   class Meta:
      model=Post
      fields = '__all__'