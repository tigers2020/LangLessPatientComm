from django import forms
from django.contrib import admin

from .models import Drug, Condition, Route


# Custom form for the Drug model to display Many-to-Many fields as checkboxes
class DrugAdminForm(forms.ModelForm):
    """
    Custom form for the Drug model in admin panel.
    Widgets are overridden to display 'uses' and 'side_effects' Many-to-Many fields as checkboxes.
    """

    class Meta:
        model = Drug
        fields = '__all__'
        widgets = {
            'uses': forms.CheckboxSelectMultiple,  # checkboxes for 'uses' field
            'side_effects': forms.CheckboxSelectMultiple,  # checkboxes for 'side_effects' field
        }


# Custom admin class for the Drug model
class DrugAdmin(admin.ModelAdmin):
    """
    Defines how the admin site should display and interact with the 'Drug' model.
    """

    form = DrugAdminForm  # Use the custom form for the Drug model

    # Define what fields to display on the list view in the admin panel
    list_display = ('brand_name', 'route')
    # Add filters on the sidebar of the list view
    list_filter = ('route', 'uses', 'side_effects')
    # Add search functionality in the list view
    search_fields = ('brand_name',)

    # Organize the fields in the form view into fieldsets with custom names
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
    Defines how the admin site should display and interact with the 'Route' model.
    """

    # Define what fields to display on the list view
    list_display = ('name', 'short_description')
    # Add filters on the sidebar of the list view
    list_filter = ('name',)
    # Add search functionality on the list view
    search_fields = ['name', 'description']
    # Define how the rows should be ordered (by 'name')
    ordering = ['name']

    @admin.display(description='Short Description')
    def short_description(self, obj):
        """
        Returns a shortened version of the description for each 'Route'. Can be used in list view.
        """
        if obj.description:
            return f"{obj.description[:50]}..."
        return "No description available"


# Custom admin class for the Condition model
class ConditionAdmin(admin.ModelAdmin):
    """
    Defines how the admin site should display and interact with the 'Condition' model.
    """

    # Define what fields to display on the list view
    list_display = ('name', 'is_side_effect', 'image_tag')
    # Add filters on the sidebar of the list view
    list_filter = ('is_side_effect',)
    # Add search functionality on the list view
    search_fields = ('name',)
    # Make 'image_tag' field read-only
    readonly_fields = ('image_tag',)


# Register the models with their corresponding admin classes in the admin site
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Drug, DrugAdmin)
