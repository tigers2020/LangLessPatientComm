from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Tag, Article

# Category admin configuration
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')  # List view fields
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    search_fields = ('name', 'description')  # Searchable fields

    def article_count(self, obj):
        """Display number of articles in category"""
        return obj.articles.count()

    article_count.short_description = 'Number of Articles'

# Tag admin configuration
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')  # List view fields
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name
    search_fields = ('name',)  # Searchable fields

    def article_count(self, obj):
        """Display number of articles with this tag"""
        return obj.articles.count()

    article_count.short_description = 'Number of Articles'

# Article admin configuration
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'status', 'publish_date',
        'view_on_site')  # List view fields
    list_filter = ('status', 'created_date', 'publish_date',
                   'category')  # Filterable fields
    search_fields = ('title', 'content', 'summary')  # Searchable fields
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug from title
    date_hierarchy = 'publish_date'  # Date-based drilldown navigation
    ordering = ('status', '-publish_date')  # Default ordering
    filter_horizontal = ('tags',)  # M2M field display
    actions = ['make_published', 'make_draft']  # Custom admin actions

    # Form layout configuration
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
        """Set author to current user on new article creation"""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def view_on_site(self, obj):
        """Generate 'View on site' link"""
        url = obj.get_absolute_url()
        return format_html('<a href="{}" target="_blank">View</a>', url)

    def make_published(self, request, queryset):
        """Bulk action: Mark selected articles as published"""
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} article(s) marked as published.')

    make_published.short_description = "Mark selected articles as published"

    def make_draft(self, request, queryset):
        """Bulk action: Mark selected articles as draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} article(s) marked as draft.')

    make_draft.short_description = "Mark selected articles as draft"