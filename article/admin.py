from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Tag, Article


# Admin configuration for the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')  # Defines fields to display in the model list view
    prepopulated_fields = {'slug': ('name',)}  # Auto-populates the slug field based on the name
    search_fields = ('name', 'description')  # Defines fields which can be searched in the admin view

    def article_count(self, obj):
        """Method to display the number of articles in each category in the admin view"""
        return obj.articles.count()  # Count of articles related to the category

    article_count.short_description = 'Number of Articles'  # Description for the method output


# Admin configuration for the Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')  # Defines fields to display in the model list view
    prepopulated_fields = {'slug': ('name',)}  # Auto-populates the slug field based on the name
    search_fields = ('name',)  # Defines fields which can be searched in the admin view

    def article_count(self, obj):
        """Method to display the number of articles associated with each tag in the admin view"""
        return obj.articles.count()  # Count of articles related to the tag

    article_count.short_description = 'Number of Articles'  # Description for the method output


# Admin configuration for the Article model
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'status', 'publish_date',
        'view_on_site')  # Defines fields to display in the model list view
    list_filter = ('status', 'created_date', 'publish_date',
                   'category')  # Defines fields that can be used for filtering the list view 
    search_fields = ('title', 'content', 'summary')  # Defines fields that can be searched in the admin view
    prepopulated_fields = {'slug': ('title',)}  # Auto-populates the slug field based on the title
    date_hierarchy = 'publish_date'  # Allows navigation of objects by date
    ordering = ('status', '-publish_date')  # Default ordering applied to the model list view
    filter_horizontal = ('tags',)  # Provides a horizontal filter for many-to-many fields
    actions = ['make_published', 'make_draft']  # Defines custom actions available for this model

    # Defines how the CRUD form is displayed
    fieldsets = (
        # Each tuple includes the title of the fieldset and a dictionary of options
        (None, {
            'fields': ('title', 'slug', 'content', 'summary')  # These fields will be displayed in a single section
        }),
        ('Publication', {
            'fields': ('status', 'publish_date', 'category', 'tags', 'featured_image'),
            'classes': ('collapse',)  # This section can be collapsed
        }),
        ('Metrics', {
            'fields': ('views_count',),
            'classes': ('collapse',)  # This section can be collapsed
        })
    )

    def save_model(self, request, obj, form, change):
        """
        Override save_model to set the Article author as the currently logged-in user 
        """
        if not change:  # If this Article is newly created (not a change to existing one)
            obj.author = request.user  # Set author to the current user
        super().save_model(request, obj, form, change)  # Continue with the default save operation

    def view_on_site(self, obj):
        """Method to display a link to view the article on the site from the admin view"""
        url = obj.get_absolute_url()  # Get the url of the article
        return format_html('<a href="{}" target="_blank">View</a>', url)  # Return a clickable HTML link

    def make_published(self, request, queryset):
        """Admin action to change the status of selected articles to 'published'"""
        updated = queryset.update(status='published')  # Update status of selected articles to 'published'
        self.message_user(request, f'{updated} article(s) marked as published.')  # Message to display after action

    make_published.short_description = "Mark selected articles as published"  # Description for the action

    def make_draft(self, request, queryset):
        """Admin action to change the status of selected articles to 'draft'"""
        updated = queryset.update(status='draft')  # Update status of selected articles to 'draft'
        self.message_user(request, f'{updated} article(s) marked as draft.')  # Message to display after action

    make_draft.short_description = "Mark selected articles as draft"  # Description for the action
