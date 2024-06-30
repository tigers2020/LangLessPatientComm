from django import forms
from django.contrib import admin

from .models import Drug, Condition, Route


# Custom form for the Drug model to display Many-to-Many fields as checkboxes
class DrugAdminForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'
        widgets = {
            'uses': forms.CheckboxSelectMultiple,
            'side_effects': forms.CheckboxSelectMultiple,
        }


# Custom admin class for the Drug model
class DrugAdmin(admin.ModelAdmin):
    form = DrugAdminForm
    list_display = ('brand_name', 'route')
    list_filter = ('route', 'uses', 'side_effects')
    search_fields = ('brand_name',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('brand_name', 'image')
        }),
        ('Route Information', {
            'fields': ('route',)
        }),
        ('Drug Details', {
            'fields': ('description', 'uses', 'dosage', 'ingredients', 'side_effects', 'full_product_details')
        }),
    )


class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description')
    list_filter = ('name',)
    search_fields = ['name', 'description']
    ordering = ['name']

    @admin.display(description='Short Description')
    def short_description(self, obj):
        if obj.description:
            return f"{obj.description[:50]}..."
        return "No description available"


# Custom admin class for the Condition model
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_side_effect', 'image_tag')
    list_filter = ('is_side_effect',)
    search_fields = ('name',)
    readonly_fields = ('image_tag',)


# Register the models with the custom admin configuration
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Drug, DrugAdmin)
