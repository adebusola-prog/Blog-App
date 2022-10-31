from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from . models import Post, Author, Category, Comment
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import CommentForm, PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import datetime
# Create your views here.

def about(request):
   context={}
   return render(request, 'ourblog/about.html', context)


def homepage(request):
   bloggers= Author.objects.all()
   items_category=Category.objects.all()
   context={'bloggers': bloggers, 'items_category': items_category}
   return render(request, "ourblog/home.html", context)
   

@login_required(login_url='login')
def blog_detailpage(request, pk):
   posts=get_object_or_404(Post, id=pk) 
   stuff= get_object_or_404(Post, id=pk)
   total_likes=stuff.total_likes()

   liked= False
   if stuff.likes.filter(id=request.user.id).exists():
      liked= True
   context={'posts':posts, 'stuff': stuff, 'total_likes': total_likes, 'liked': liked}
   return render(request, 'ourblog/detail-page.html', context)


@login_required(login_url='login')
def comment_detailpage(request, pk):
   posts=get_object_or_404(Post, id=pk)

   if request.method == "POST":
      form = CommentForm(request.POST)

      if form.is_valid(): 
         comment= form.save(commit=False)
         comment.post=posts      #comment.post('the post model')
         comment.name = request.user
         comment.save()
         return redirect('blog_detail', pk=posts.id)
   else:
      form= CommentForm()
   
   context={'detail_posts':posts, 'form':form}
   return render(request, 'ourblog/comment_detail.html', context)

@login_required(login_url='login')
def author_detailpage(request, pk):
   author=get_object_or_404(Author, id=pk)
   context={'author':author}
   return render(request, 'ourblog/author-detail.html', context)

@login_required(login_url='login')
def blogpage(request):
   q= request.GET.get('q', '') 
   posts=Post.active_objects.filter(created_at__lte=datetime.date.today()).filter(
   Q(author__first_name__icontains=q)|
   Q(title__icontains=q)| 
   Q(description__icontains=q)
   )
   context={'posts':posts, 'q': q}
   
   return render(request, 'ourblog/blogger.html', context)


def loginpage(request):
   if request.user.is_authenticated:
      return redirect('blogpage')

   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      try:
         user=User.objects.get(username=username)
      except:
         messages.error(request, 'User does not exist') 
      
      user = authenticate(request, username=username, password=password)
         
      if user is not None:
         login(request, user)
         return redirect('blogpage')

      else:
         messages.error(request, 'Username OR password does not exist')
   
   context={}
   return render(request, 'ourblog/login_register.html', context)

def logoutUser(request):
   logout(request)
   return redirect('home')

def registerPage(request):
   form =UserCreationForm

   if request.method=="POST":
      form=UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False) #it's like freezing, you want to be able to access the user
         user.username=user.username
         user.save()
         login(request, user)
         return redirect('home')
      else:
         messages.error(request,  "An error occured during registration")
   
   return render(request, 'ourblog/login_register.html', {'form': form})


def category_detail(request, pk):
   category= get_object_or_404(Category, id=pk)
   
   context={'category': category}

   return render(request, 'ourblog/category.html', context)


class PostCreate(PermissionRequiredMixin, CreateView):
   model=Post
   template_name = 'ourblog/post_create.html'
   fields= '__all__'
   permission_required = ('ourblog.can_create_post',) 
   queryset=Post.objects.all()
   sucess_url= reverse_lazy('blogpager')

class PostUpdate(PermissionRequiredMixin, UpdateView):
   model=Post
   permission_required = ('ourblog.can_update_post',)
   template_name= 'ourblog/post_create.html'
   fields= '__all__'

class PostDelete(PermissionRequiredMixin, DeleteView):
   model=Post
   permission_required= ('ourblog.can_delete_post',)
   template_name = 'ourblog/post_delete.html'

   success_url = reverse_lazy('blogpage')   

@login_required
def post_update(request, pk):
   
   post= Post.objects.get(id=pk)
   form = PostForm(instance=post)

   if request.user != post.author.user and request.user.is_superuser==False:
      return HttpResponse('You are not allowed here!!!')
   
   if request.method == "POST":
      form=PostForm(request.POST, instance=post)
      if form.is_valid():
         form.save()
         return redirect('blogpage')

   context={'post':post, 'form':form}
   return render(request, 'ourblog/post_create.html', context)


@login_required
def post_create(request):
   form=PostForm()

   if request.method== "POST":
      form= PostForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('blogpage')

   context={'form': form} 
   return render(request, 'ourblog/post_create.html', context)


@login_required
def post_delete(request, pk):
   post =get_object_or_404(Post, id=pk)
   
   if request.user != post.author.user and not request.user.is_superuser:
      return HttpResponse('You are not allowed here!!!')

   if request.method == "POST":
      post.is_active = False
      post.save()
      return redirect('home')

   context={'post':post}
   return render(request, 'ourblog/post_delete.html', context)        

@login_required
def restore_post(request, pk):
   post=get_object_or_404(Post, id=pk)

   if request.user != post.author.user and not request.user.is_superuser:
      return HttpResponse('You are not allowed here!!!')

   if request.method =="POST":
      post.is_active=True
      post.save()

      return redirect('blogpage')

   context={'post':post}
   return render(request, 'ourblog/restore.html', context)

def inactive_posts(request):
   post_inactive=Post.inactive_objects.all()
   context={'post_inactive':post_inactive}
   return render(request, 'ourblog/non_active_post.html', context)
   

def like_views(request, pk):   
   post_like= get_object_or_404(Post, id=pk)
   liked = False
   if post_like.likes.filter(id=request.user.id).exists():
      post_like.likes.remove(request.user)
      liked= False
   else:
      post_like.likes.add(request.user)
      liked = True

   return HttpResponseRedirect(reverse('blog_detail', args=str(pk)))