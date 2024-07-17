import re

from django.contrib import admin

from doctors.models import Doctor, Specialty


# Register your models here.
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# doctors/admin.py

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('provider_first_name', 'provider_last_name', 'formatted_phone_number', 'primary_specialty')

    def formatted_phone_number(self, obj):
        phone_number = str(obj.telephone_number)
        phone_number = re.sub(r'\D', '', phone_number)
        if len(phone_number) == 10:  # Assuming US phone number format
            formatted_number = f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
        else:
            formatted_number = phone_number  # Return the original if it doesn't match the expected length
        return formatted_number

    formatted_phone_number.short_description = 'Phone Number'
