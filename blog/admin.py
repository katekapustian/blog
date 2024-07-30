from django.contrib import admin
from .models import Post, Category, Tag, Comment, Subscriber, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'category', 'user')
    list_filter = ('published_date', 'category')
    search_fields = ('title', 'content')
    inlines = [PostImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('text', 'author')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass
