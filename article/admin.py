# article/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model
    """
    list_display = ('name', 'slug', 'article_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def article_count(self, obj):
        """Display the number of articles in each category"""
        return obj.articles.count()
    article_count.short_description = 'Number of Articles'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model
    """
    list_display = ('name', 'slug', 'article_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def article_count(self, obj):
        """Display the number of articles for each tag"""
        return obj.articles.count()
    article_count.short_description = 'Number of Articles'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Article model
    """
    list_display = ('title', 'category', 'status', 'publish_date', 'view_on_site')
    list_filter = ('status', 'created_date', 'publish_date', 'category')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    ordering = ('status', '-publish_date')
    filter_horizontal = ('tags',)
    actions = ['make_published', 'make_draft']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'summary')
        }),
        ('Publication', {
            'fields': ('status', 'publish_date', 'category', 'tags', 'featured_image'),
            'classes': ('collapse',)
        }),
        ('Metrics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        """
        Override save_model to set the author as the current user
        """
        if not change:  # If this is a new article
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def view_on_site(self, obj):
        """Provide a link to view the article on the site"""
        url = obj.get_absolute_url()
        return format_html('<a href="{}" target="_blank">View</a>', url)

    def make_published(self, request, queryset):
        """Admin action to mark selected articles as published"""
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} article(s) marked as published.')
    make_published.short_description = "Mark selected articles as published"

    def make_draft(self, request, queryset):
        """Admin action to mark selected articles as draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} article(s) marked as draft.')
    make_draft.short_description = "Mark selected articles as draft"