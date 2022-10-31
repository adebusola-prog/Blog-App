from django.urls import path
from . import views
# from ourblog.views import PostCreate, PostUpdate, PostDelete

urlpatterns=[
  
   path('',  views.homepage, name="home"),
   path('about/',  views.about, name="about"),
   path('category/<int:pk>/',  views.category_detail, name="category_detail"),
   path('blog_detail/<int:pk>/',  views.blog_detailpage, name="blog_detail"),
   path('comment_detail/<int:pk>/',  views.comment_detailpage, name="comment_detail"),
   path('author_detail/<int:pk>/',  views.author_detailpage, name="author_detail"),
   path('blogger/',  views.blogpage, name="blogpage"),
  
   path("login/", views.loginpage, name="login"),
   path("logout/", views.logoutUser, name="logout"),
   path("register/", views.registerPage, name="register"),
   
   path("post/<int:pk>/update/", views.post_update, name="post_update"),
   path("post/create/", views.post_create, name="post_create"),
   path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
   path("post/inactive/", views.inactive_posts, name="inactive_posts"),
   path("post/<int:pk>/restore/", views.restore_post, name="restore_post"),
   path("like/<int:pk>/", views.like_views, name="like_post"),

]
