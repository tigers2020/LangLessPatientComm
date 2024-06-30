from django import forms
from django.contrib import admin

from .models import Drug, Symptom, SideEffect, Route


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


class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    readonly_fields = ('image_tag',)


class SideEffectAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    readonly_fields = ('image_tag',)


# Register the models with the custom admin configuration
admin.site.register(Symptom, SymptomAdmin)
admin.site.register(SideEffect, SideEffectAdmin)
admin.site.register(Route)
admin.site.register(Drug, DrugAdmin)
