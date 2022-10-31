from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse

class ActiveManager(models.Manager):

   def get_queryset(self):
      return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):
   
   def get_queryset(self):
      return super().get_queryset().filter(is_active=False)

      
class Author(models.Model):
   user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   first_name= models.CharField(max_length=200)
   last_name=models.CharField(max_length=200)
   email=models.EmailField(max_length=200, unique=True)
   bio=models.TextField()
   is_active = models.BooleanField(default=True)

   objects = models.Manager()
   active_objects = ActiveManager()
   inactive_objects =InActiveManager()


   def __str__(self):
      return self.first_name + " " + self.last_name

   def get_absolute_url(self):
      return reverse('author_detail', args=[str(self.id)])

   def authors(self):
      return Post.active_objects.filter(author_id=self.id)  #instead of using author.post_set.all--> you use---(authors(name of the fxn. 
                                                               # you can then say for author in authors...))

   
class Category(models.Model):
   name=models.CharField(max_length=100)
   slug=models.SlugField()
   is_active = models.BooleanField(default=True)

   objects = models.Manager()
   active_objects = ActiveManager()
   inactive_objects =InActiveManager()

   def categories(self):
      return Post.active_objects.filter(category_id=self.id)


   class Meta:
      verbose_name_plural= "Categories"

   def __str__(self):
      return self.name

   def get_absolute_url(self):
      return reverse('blog_detail', args=[str(self.id)])


class Post(models.Model):
   title=models.CharField(max_length=200)
   slug=models.SlugField()
   intro=models.CharField(max_length=400)
   description=models.TextField()
   created_at=models.DateTimeField(auto_now_add=False)
   updated_at=models.DateTimeField(auto_now=True)
   author=models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
   category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
   image=models.ImageField(upload_to='uploads/', blank=True, null=True)
   is_active = models.BooleanField(default=True)
   likes= models.ManyToManyField(User)



   objects = models.Manager()
   active_objects = ActiveManager()
   inactive_objects =InActiveManager()

   class Meta:
      ordering=['-created_at']
      permissions=(("can_create_post", "Set to create post"),)
      permissions=(("can_update_post", "Set to update post"),)
      permissions=(("can_delete_post", "Set to delete post"),)


   def total_likes(self):
      return self.likes.count()


   def __str__(self):
      return self.title

   def get_absolute_url(self):
      return reverse('blog_detail', args=[str(self.id)])

   def comments(self):
      return Comment.active_objects.filter(post_id=self.id)

   

class Comment(models.Model):
   name=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   email=models.EmailField()
   description=models.TextField(help_text="Kindly write your comments here")
   post=models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
   created_at=models.DateTimeField(auto_now_add=True)
   is_active = models.BooleanField(default=False)


   objects = models.Manager()
   active_objects = ActiveManager()
   inactive_objects =InActiveManager()

   class Meta:
      ordering=['-created_at']

   def __str__(self):
      return 'Comment {} by {}' .format(self.description, self.name)
   



