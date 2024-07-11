from django.contrib import admin

from doctors.models import Doctor, Specialty


# Register your models here.
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['provider_first_name', 'provider_last_name', 'primary_specialty']
    search_fields = ['provider_first_name', 'provider_last_name', 'primary_specialty__name']
