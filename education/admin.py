# File: education/admin.py

from django.contrib import admin

from .models import Scenario, Page, Image, Choice, Outcome


class ImageInline(admin.TabularInline):
    """
    Inline configuration for Image model.
    Allows adding images directly within the parent model's admin page.
    """
    model = Image
    extra = 1  # Number of extra empty forms to display


class ChoiceInline(admin.TabularInline):
    """
    Inline configuration for Choice model.
    Allows adding choices directly within the parent model's admin page.
    """
    model = Choice
    extra = 1  # Number of extra empty forms to display
    fk_name = 'page'  # Specify foreign key relationship


class PageInline(admin.TabularInline):
    """
    Inline configuration for Page model.
    Allows adding pages directly within the parent model's admin page.
    """
    model = Page
    extra = 1  # Number of extra empty forms to display


class OutcomeInline(admin.TabularInline):
    """
    Inline configuration for Outcome model.
    Allows adding outcomes directly within the parent model's admin page.
    """
    model = Outcome
    extra = 1  # Number of extra empty forms to display


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Scenario model.
    """
    list_display = ('title', 'created_at', 'updated_at')  # Fields to display in the list view
    search_fields = ('title',)  # Enable search by title
    inlines = [PageInline]  # Display Page inlines within Scenario admin page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Page model.
    """
    list_display = ('scenario', 'order')  # Fields to display in the list view
    list_filter = ('scenario',)  # Enable filtering by scenario
    inlines = [ImageInline, ChoiceInline,
               OutcomeInline]  # Display Image, Choice, and Outcome inlines within Page admin page
    search_fields = ('scenario__title', 'content')  # Enable search by scenario title and content


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Image model.
    """
    list_display = ('page', 'caption', 'order')  # Fields to display in the list view
    list_filter = ('page',)  # Enable filtering by page
    search_fields = ('caption',)  # Enable search by caption


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Choice model.
    """
    list_display = ('page', 'text', 'next_page')  # Fields to display in the list view
    list_filter = ('page',)  # Enable filtering by page
    search_fields = ('text',)  # Enable search by text


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Outcome model.
    """
    list_display = ('page', 'is_end', 'next_scenario')  # Fields to display in the list view
    list_filter = ('is_end',)  # Enable filtering by end status
    search_fields = ('description',)  # Enable search by description
