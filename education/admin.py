# src/education/admin.py

# Import necessary modules
from django.contrib import admin
from .models import Scenario, Page, Image, Choice, Outcome


# Image sections in the admin interface for a particular Scenario, Page, etc.
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Number of extra empty forms


# Choice sections in the admin interface for a particular Scenario, Page, etc.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fk_name = 'page'

# Page sections in the admin interface for a particular Scenario


class PageInline(admin.TabularInline):
    model = Page
    extra = 1


# Outcome sections in the admin interface for a particular Scenario, Page, etc.
class OutcomeInline(admin.TabularInline):
    model = Outcome
    extra = 1


# Register Scenario to admin site. Customize the admin interface for Scenario model.
@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')  # Fields to display in list view
    search_fields = ('title',)  # Searchable fields
    inlines = [PageInline]  # Display Page inlines


# Register Page to admin site. Customize the admin interface for Page model.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'order')  # Fields to display in list view
    list_filter = ('scenario',)  # Fields for list filter
    inlines = [ImageInline, ChoiceInline, OutcomeInline]  # Display Image, Choice and Outcome inlines
    search_fields = ('scenario__title', 'content')  # Searchable fields


# Register Image to admin site. Customize the admin interface for Image model.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('page', 'caption', 'order')  # Fields to display in list view
    list_filter = ('page',)  # Fields for list filter
    search_fields = ('caption',)  # Searchable fields


# Register Choice to admin site. Customize the admin interface for Choice model.
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('page', 'text', 'next_page')  # Fields to display in list view
    list_filter = ('page',)  # Fields for list filter
    search_fields = ('text',)  # Searchable fields


# Register Outcome to admin site. Customize the admin interface for Outcome model.
@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('page', 'is_end', 'next_scenario')  # Fields to display in list view
    list_filter = ('is_end',)  # Fields for list filter
    search_fields = ('description',)  # Searchable fields
