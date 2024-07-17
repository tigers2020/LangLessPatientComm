# doctors/templatetags/custom_filters.py

from django import template
import re

register = template.Library()


@register.filter
def phone_format(value):
    phone_number = str(value)  # Ensure the value is a string

    # Remove non-numeric characters
    phone_number = re.sub(r'\D', '', phone_number)

    # Format the phone number
    if len(phone_number) == 10:  # Assuming US phone number format
        formatted_number = f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
    else:
        formatted_number = value  # Return the original if it doesn't match the expected length

    return formatted_number
