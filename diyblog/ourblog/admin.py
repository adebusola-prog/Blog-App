from django.contrib import admin
from ourblog.models import Author, Comment, Category, Post
# Register your models here.

class CommentItemInline(admin.TabularInline):
   model=Comment

class PostAdmin(admin.ModelAdmin):
   search_fields= ['title, description, author, category']
   list_display=['title', 'slug', 'category', 'author']
   list_filter= ['category', 'author', 'created_at']
   inlines=[CommentItemInline]
   prepopulated_fields={'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
   search_fields=['name']
   list_display=['name']
   prepopulated_fields={'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
   list_display=['name', 'description', 'post', 'created_at']
   list_filter= ['created_at']
   search_fields=['name', 'email', 'description']
   # actions = ['approve_comments']

   # def approve_comments(self, request, queryset):
   #    queryset.update(active=True)



admin.site.register(Author)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
