from django.contrib import admin
from .models import Post, Category, Comment

# Customize the admin interface for the Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    list_filter = ('author', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Customize the admin interface for the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# Customize the admin interface for the Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('content',)

# Register the models with their custom admin classes
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
