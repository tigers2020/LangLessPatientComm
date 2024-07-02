# src/education/admin.py

from django.contrib import admin

from .models import Scenario, Page, Image, Choice, Outcome


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fk_name = 'page'


class PageInline(admin.TabularInline):
    model = Page
    extra = 1


class OutcomeInline(admin.TabularInline):
    model = Outcome
    extra = 1


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [PageInline]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'order')
    list_filter = ('scenario',)
    inlines = [ImageInline, ChoiceInline, OutcomeInline]
    search_fields = ('scenario__title', 'content')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('page', 'caption', 'order')
    list_filter = ('page',)
    search_fields = ('caption',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('page', 'text', 'next_page')
    list_filter = ('page',)
    search_fields = ('text',)


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('page', 'is_end', 'next_scenario')
    list_filter = ('is_end',)
    search_fields = ('description',)
