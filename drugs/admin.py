# File: drugs/admin.py

from django import forms
from django.contrib import admin
from .models import Drug, Condition, Route

class DrugAdminForm(forms.ModelForm):
    """
    Custom form for Drug model in the admin panel.
    Overrides default widgets to use checkboxes for 'uses' and 'side_effects' fields,
    improving usability for multiple selections.
    """
    class Meta:
        model = Drug
        fields = '__all__'
        widgets = {
            'uses': forms.CheckboxSelectMultiple,  # Use checkboxes for 'uses' field
            'side_effects': forms.CheckboxSelectMultiple,  # Use checkboxes for 'side_effects' field
        }

class DrugAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Drug model.
    Uses a custom form to enhance widget display for multiple selections.
    """
    form = DrugAdminForm
    list_display = ('brand_name', 'route')  # Fields shown in the admin list view
    list_filter = ('route', 'uses', 'side_effects')  # Enable filtering in the admin interface
    search_fields = ('brand_name',)  # Enable search by brand name

    # Organize fields into logical groups in the admin detail view
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
    """
    Admin configuration for the Route model.
    """
    list_display = ('name', 'short_description')  # Show name and short description in the list view
    list_filter = ('name',)  # Allow filtering by name
    search_fields = ['name', 'description']  # Enable search by name and description
    ordering = ['name']  # Default ordering by name

    @admin.display(description='Short Description')
    def short_description(self, obj):
        """
        Generate a truncated description for display in the admin list view.
        Limits description to 50 characters for readability.
        """
        if obj.description:
            return f"{obj.description[:50]}..."  # Truncate description to 50 characters
        return "No description available"

class ConditionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Condition model.
    """
    list_display = ('name', 'is_side_effect', 'image_tag')  # Fields shown in the list view
    list_filter = ('is_side_effect',)  # Allow filtering by side effect status
    search_fields = ('name',)  # Enable search by condition name
    readonly_fields = ('image_tag',)  # Prevent editing of the image_tag field

# Register models with their custom admin classes
# This determines how each model is displayed and managed in the admin interface
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Drug, DrugAdmin)
