from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Tag, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('name', 'slug', 'article_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def article_count(self, obj):
        """
        Returns the number of articles in this category.
        """
        return obj.articles.count()

    article_count.short_description = 'Number of Articles'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model.
    """
    list_display = ('name', 'slug', 'article_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def article_count(self, obj):
        """
        Returns the number of articles associated with this tag.
        """
        return obj.articles.count()

    article_count.short_description = 'Number of Articles'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Article model.
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
            'classes': ('collapse',)  # Collapse this section by default
        }),
        ('Metrics', {
            'fields': ('views_count',),
            'classes': ('collapse',)  # Collapse this section by default
        })
    )

    def save_model(self, request, obj, form, change):
        """
        Sets the author to the current user on article creation.
        """
        if not change:
            obj.author = request.user  # Set author only if the article is new
        super().save_model(request, obj, form, change)

    def view_on_site(self, obj):
        """
        Returns a formatted HTML link to view the article on the site.
        """
        url = obj.get_absolute_url()  # Get the URL of the article
        return format_html('<a href="{}" target="_blank">View</a>', url)  # Return the link as HTML

    def make_published(self, request, queryset):
        """
        Custom admin action to mark selected articles as published.
        """
        updated = queryset.update(status='published')  # Update the status of selected articles
        self.message_user(request, f'{updated} article(s) marked as published.')  # Display a message to the admin

    make_published.short_description = "Mark selected articles as published"

    def make_draft(self, request, queryset):
        """
        Custom admin action to mark selected articles as draft.
        """
        updated = queryset.update(status='draft')  # Update the status of selected articles
        self.message_user(request, f'{updated} article(s) marked as draft.')  # Display a message to the admin

    make_draft.short_description = "Mark selected articles as draft"
