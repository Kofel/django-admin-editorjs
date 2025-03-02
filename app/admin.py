from django.contrib import admin
from app.forms import PostAdminForm
from app.models import Category, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    form = PostAdminForm
    fields = (
        'publish', 'title', 'post_id',
        'content_editor', 'category', 'slug'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    fieldsets = (
        ('Base', {
            'fields': ('name', 'title', 'snippet', 'slug', 'menu')
        }),
    )
